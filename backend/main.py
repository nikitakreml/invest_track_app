from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import date, timedelta

from . import crud, models, schemas, google_sheets
from .database import SessionLocal, engine
from .tinkoff_invest import get_asset_price_by_date, get_current_asset_price # Import the new function

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",  # Your Vue.js frontend origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dummy user for now, until authentication is implemented
def get_current_user_id(db: Session = Depends(get_db)) -> int:
    user = crud.get_user(db, user_id=1)
    if not user:
        user = crud.create_user(db, schemas.UserCreate(email="test@example.com", password="testpassword"))
    return user.id


@app.get("/users/me/settings", response_model=schemas.UserSettings)
def get_user_settings(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserSettings(
        google_sheets_api_key=user.google_sheets_api_key,
        google_sheets_spreadsheet_id=user.google_sheets_spreadsheet_id,
        tinkoff_invest_api_token=user.tinkoff_invest_api_token,
        auto_transaction_price_enabled=user.auto_transaction_price_enabled,
        balance=user.balance # Include balance in settings
    )

@app.put("/users/me/settings", response_model=schemas.UserSettings)
def update_user_settings_endpoint(
    settings: schemas.UserSettings,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = crud.update_user_settings(db, user_id, settings)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserSettings(
        google_sheets_api_key=user.google_sheets_api_key,
        google_sheets_spreadsheet_id=user.google_sheets_spreadsheet_id,
        tinkoff_invest_api_token=user.tinkoff_invest_api_token,
        auto_transaction_price_enabled=user.auto_transaction_price_enabled,
        balance=user.balance # Include balance in settings
    )

@app.post("/users/me/top-up", response_model=schemas.User)
def top_up_account(
    request: schemas.TopUpWithdrawRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    if request.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")
    user = crud.update_user_balance(db, user_id, request.amount)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/me/withdraw", response_model=schemas.User)
def withdraw_from_account(
    request: schemas.TopUpWithdrawRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    if request.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")
    user = crud.update_user_balance(db, user_id, -request.amount) # Subtract amount for withdrawal
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/transactions", response_model=List[schemas.Transaction])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    transactions = crud.get_transactions(db, skip=skip, limit=limit)
    return transactions


@app.post("/transactions", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    db_asset = crud.get_asset_by_ticker(db, transaction.asset_name)
    if not db_asset:
        db_asset = crud.create_asset(db, schemas.AssetCreate(name=transaction.asset_name, ticker=transaction.asset_name))
    
    portfolios = crud.get_portfolios(db, user_id)
    if not portfolios:
        db_portfolio = crud.create_user_portfolio(db, schemas.PortfolioCreate(name="Default Portfolio"), user_id)
    else:
        db_portfolio = portfolios[0]
    
    new_transaction = crud.create_transaction(
        db=db,
        date=transaction.date,
        type=transaction.type,
        price=transaction.price,
        asset_id=db_asset.id,
        portfolio_id=db_portfolio.id
    )

    # Adjust user balance based on transaction type
    if new_transaction.type == "Buy":
        crud.update_user_balance(db, user_id, -new_transaction.price) # Debit for buy
    elif new_transaction.type == "Sell":
        crud.update_user_balance(db, user_id, new_transaction.price) # Credit for sell

    db.refresh(new_transaction)
    return new_transaction


@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Fetch old transaction to reverse its effect on balance
    old_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if old_transaction:
        if old_transaction.type == "Buy":
            crud.update_user_balance(db, user_id, old_transaction.price) # Credit back old buy amount
        elif old_transaction.type == "Sell":
            crud.update_user_balance(db, user_id, -old_transaction.price) # Debit back old sell amount

    db_asset = crud.get_asset_by_ticker(db, transaction.asset_name)
    if not db_asset:
        db_asset = crud.create_asset(db, schemas.AssetCreate(name=transaction.asset_name, ticker=transaction.asset_name))
    
    portfolios = crud.get_portfolios(db, user_id)
    if not portfolios:
        db_portfolio = crud.create_user_portfolio(db, schemas.PortfolioCreate(name="Default Portfolio"), user_id)
    else:
        db_portfolio = portfolios[0]
    
    updated_transaction = crud.update_transaction(
        db=db,
        transaction_id=transaction_id,
        date=transaction.date,
        type=transaction.type,
        price=transaction.price,
        asset_id=db_asset.id,
        portfolio_id=db_portfolio.id
    )
    if not updated_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Apply new transaction's effect on balance
    if updated_transaction.type == "Buy":
        crud.update_user_balance(db, user_id, -updated_transaction.price) # Debit for new buy
    elif updated_transaction.type == "Sell":
        crud.update_user_balance(db, user_id, updated_transaction.price) # Credit for new sell

    db.refresh(updated_transaction)
    return updated_transaction


@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    db_transaction = crud.delete_transaction(db, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    # Revert balance change for the deleted transaction
    user_id = get_current_user_id(db) # Get user_id again as it's not passed directly
    if db_transaction.type == "Buy":
        crud.update_user_balance(db, user_id, db_transaction.price) # Credit back for deleted buy
    elif db_transaction.type == "Sell":
        crud.update_user_balance(db, user_id, -db_transaction.price) # Debit back for deleted sell

    return {"message": "Transaction deleted"}


@app.get("/portfolio/summary")
def get_portfolio_summary(
    period: str = "all_time",
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Calculate start date based on the period
    today = date.today()
    start_date = None
    if period == "day":
        start_date = today - timedelta(days=1)
    elif period == "month":
        start_date = today - timedelta(days=30)
    elif period == "year":
        start_date = today - timedelta(days=365)
    
    user_portfolios = crud.get_portfolios(db, user_id)
    if not user_portfolios:
        return {
            "period": period,
            "current_total": 0,
            "rate_of_return": 0,
            "message": "No portfolios found for this user."
        }

    all_transactions = []
    for portfolio in user_portfolios:
        query = db.query(models.Transaction).options(joinedload(models.Transaction.asset)).filter(models.Transaction.portfolio_id == portfolio.id)
        if start_date:
            query = query.filter(models.Transaction.date >= start_date)
        transactions_for_portfolio = query.all()
        all_transactions.extend(transactions_for_portfolio)

    if not all_transactions:
        return {
            "period": period,
            "current_total": 0,
            "rate_of_return": 0,
            "message": "No transactions found for this period."
        }

    current_total = 0.0
    initial_investment = 0.0

    for transaction in all_transactions:
        if transaction.type == "Buy":
            current_total -= transaction.price # Outflow
            initial_investment += transaction.price
        elif transaction.type == "Sell":
            current_total += transaction.price # Inflow
    
    rate_of_return = 0.0
    if initial_investment > 0:
        # The current_total here represents the net change based on buy/sell prices.
        # To calculate rate of return, we should consider the *profit/loss* relative to the *initial investment*.
        # Simplified: (current_value - initial_investment) / initial_investment
        # For now, let's assume current_total is the 'current_value' minus the initial_investment for simplicity in this stub.
        # This needs more robust logic for actual portfolio performance.
        # If current_total is the net of buys and sells, then the 'profit' is `current_total`.
        profit = current_total # If positive, it's profit, if negative, it's loss
        rate_of_return = (profit / initial_investment) * 100

    return {
        "period": period,
        "current_total": round(current_total, 2),
        "rate_of_return": round(rate_of_return, 2), # As percentage
        "message": "Portfolio summary calculated."
    }


@app.get("/portfolio/composition")
def get_portfolio_composition(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.tinkoff_invest_api_token:
        return {"composition": [], "total_portfolio_value": user.balance, "message": "Tinkoff Invest API token not set. Cannot fetch live asset prices."}

    user_portfolios = crud.get_portfolios(db, user_id)
    if not user_portfolios:
        return {"composition": [{"name": "Cash (Balance)", "value": round(user.balance, 2)}], "total_portfolio_value": user.balance, "message": "No portfolios found. Displaying only cash balance."}

    # For simplicity, assume one default portfolio for now
    default_portfolio = user_portfolios[0]
    
    # Calculate current holdings of each asset
    asset_holdings = {}
    transactions = db.query(models.Transaction).options(joinedload(models.Transaction.asset)).filter(models.Transaction.portfolio_id == default_portfolio.id).all()

    for transaction in transactions:
        ticker = transaction.asset.ticker
        if ticker not in asset_holdings:
            asset_holdings[ticker] = {"name": transaction.asset.name, "quantity": 0.0, "value": 0.0}
        
        if transaction.type == "Buy":
            asset_holdings[ticker]["quantity"] += 1 # Assuming 1 unit per transaction for simplicity
        elif transaction.type == "Sell":
            asset_holdings[ticker]["quantity"] -= 1

    composition_data = []
    total_portfolio_value = user.balance

    # Add cash balance to composition
    composition_data.append(["Cash (Balance)", round(user.balance, 2)])

    # Calculate current value of each asset holding
    for ticker, data in asset_holdings.items():
        if data["quantity"] > 0:
            current_price = get_current_asset_price(ticker, user.tinkoff_invest_api_token)
            if current_price is not None and data["name"] is not None:
                asset_value = data["quantity"] * current_price
                composition_data.append([data["name"], round(asset_value, 2)])
                total_portfolio_value += asset_value
            elif data["name"] is not None: # Asset held, but price unavailable
                composition_data.append([f"{data['name']} (Price Unavailable)", 0.0]) # Still show asset, but with 0 value
            else: # Fallback if asset name is also None
                composition_data.append([f"{ticker} (Name/Price Unavailable)", 0.0])

    return {"composition": composition_data, "total_portfolio_value": round(total_portfolio_value, 2), "message": "Portfolio composition calculated."}


@app.get("/asset/estimate-price")
def estimate_asset_price(
    ticker: str,
    target_date: date,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = crud.get_user(db, user_id)
    if not user or not user.tinkoff_invest_api_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tinkoff Invest API token not set for user")
    
    price = get_asset_price_by_date(ticker, target_date, user.tinkoff_invest_api_token)
    
    if price is None:
        raise HTTPException(status_code=404, detail=f"Could not retrieve price for {ticker} on {target_date}.")
    
    return {"ticker": ticker, "date": target_date, "price": price}

@app.get("/google_sheets/read_transactions")
def read_sheets_transactions(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = crud.get_user(db, user_id)
    if not user or not user.google_sheets_api_key or not user.google_sheets_spreadsheet_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google Sheets API key or Spreadsheet ID not set for user")
    
    transactions_from_sheets = google_sheets.read_transactions_from_sheets(user.google_sheets_api_key, user.google_sheets_spreadsheet_id)
    return {"transactions": transactions_from_sheets}

@app.post("/google_sheets/write_transaction")
def write_sheets_transaction(
    transaction_data: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = crud.get_user(db, user_id)
    if not user or not user.google_sheets_api_key or not user.google_sheets_spreadsheet_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google Sheets API key or Spreadsheet ID not set for user")
    
    google_sheets.write_transaction_to_sheets(user.google_sheets_api_key, user.google_sheets_spreadsheet_id, transaction_data.model_dump())
    return {"message": "Transaction written to Google Sheets (stub)"}
