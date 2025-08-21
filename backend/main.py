from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas, google_sheets
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
    user_id: int = Depends(get_current_user_id) # user_id will be used later for portfolios
):
    # For now, let's ensure the asset exists or create it
    db_asset = crud.get_asset_by_ticker(db, transaction.asset_name) # Assuming asset_name is passed in transaction for simplicity here
    if not db_asset:
        db_asset = crud.create_asset(db, schemas.AssetCreate(name=transaction.asset_name, ticker=transaction.asset_name))
    transaction.asset_id = db_asset.id

    # For now, let's assume a default portfolio for the user, or create one.
    # In a real app, this would be selected by the user.
    portfolios = crud.get_portfolios(db, user_id)
    if not portfolios:
        db_portfolio = crud.create_user_portfolio(db, schemas.PortfolioCreate(name="Default Portfolio"), user_id)
    else:
        db_portfolio = portfolios[0]
    transaction.portfolio_id = db_portfolio.id
    
    return crud.create_transaction(db=db, transaction=transaction)


@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    db_transaction = crud.update_transaction(db, transaction_id, transaction)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction


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
    # This is a stub for portfolio performance analysis.
    # In a real application, you would fetch transactions for the user's portfolios,
    # calculate performance based on the selected period, and potentially fetch
    # current prices for assets.
    return {"period": period, "returns": "N/A", "message": "Portfolio summary calculation is not yet implemented."}


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
