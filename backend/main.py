from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import date

from . import crud, models, schemas, google_sheets
from .database import SessionLocal, engine

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
        user = crud.create_user(db, schemas.UserCreate())
    return user.id


@app.post("/auth/set-key")
def set_google_sheets_api_key(
    api_key: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = crud.update_user_api_key(db, user_id, api_key)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Google Sheets API key updated successfully"}


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
    db.refresh(new_transaction)
    return new_transaction


@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int,
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
    return {"message": "Transaction deleted"}


@app.get("/portfolio/summary")
def get_portfolio_summary(
    period: str = "all_time",
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Get all transactions for the user's portfolios
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
        transactions_for_portfolio = db.query(models.Transaction).options(joinedload(models.Transaction.asset)).filter(models.Transaction.portfolio_id == portfolio.id).all()
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
    
    # For simplicity, current_total will be the net of buys and sells.
    # In a real app, this would consider current asset values.

    rate_of_return = 0.0
    if initial_investment > 0:
        rate_of_return = (current_total / initial_investment) # This is a simplified calculation

    return {
        "period": period,
        "current_total": round(current_total, 2),
        "rate_of_return": round(rate_of_return * 100, 2), # As percentage
        "message": "Portfolio summary calculated."
    }


@app.get("/google_sheets/read_transactions")
def read_sheets_transactions(
    spreadsheet_id: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = crud.get_user(db, user_id)
    if not user or not user.google_sheets_api_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google Sheets API key not set for user")
    
    transactions_from_sheets = google_sheets.read_transactions_from_sheets(user.google_sheets_api_key, spreadsheet_id)
    return {"transactions": transactions_from_sheets}

@app.post("/google_sheets/write_transaction")
def write_sheets_transaction(
    spreadsheet_id: str,
    transaction_data: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = crud.get_user(db, user_id)
    if not user or not user.google_sheets_api_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google Sheets API key not set for user")
    
    google_sheets.write_transaction_to_sheets(user.google_sheets_api_key, spreadsheet_id, transaction_data.model_dump())
    return {"message": "Transaction written to Google Sheets (stub)"}
