from sqlalchemy.orm import Session, joinedload
from datetime import date
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password # In a real app, hash this password
    db_user = models.User(email=user.email, hashed_password=hashed_password, balance=0.0) # Initialize balance
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_settings(db: Session, user_id: int, settings: schemas.UserSettings):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = settings.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def update_user_balance(db: Session, user_id: int, amount: float):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.balance += amount
        db.commit()
        db.refresh(db_user)
    return db_user

def update_user_api_key(db: Session, user_id: int, api_key: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.google_sheets_api_key = api_key
        db.commit()
        db.refresh(db_user)
    return db_user

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).options(joinedload(models.Transaction.asset)).offset(skip).limit(limit).all()

def create_transaction(db: Session, date: date, type: str, price: float, asset_id: int, portfolio_id: int):
    db_transaction = models.Transaction(date=date, type=type, price=price, asset_id=asset_id, portfolio_id=portfolio_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    # Load the asset relationship after refresh
    db_transaction_with_asset = db.query(models.Transaction).options(joinedload(models.Transaction.asset)).filter(models.Transaction.id == db_transaction.id).first()
    return db_transaction_with_asset

def update_transaction(db: Session, transaction_id: int, date: date, type: str, price: float, asset_id: int, portfolio_id: int):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction:
        db_transaction.date = date
        db_transaction.type = type
        db_transaction.price = price
        db_transaction.asset_id = asset_id
        db_transaction.portfolio_id = portfolio_id
        db.commit()
        db.refresh(db_transaction)
        # Load the asset relationship after refresh
        db_transaction_with_asset = db.query(models.Transaction).options(joinedload(models.Transaction.asset)).filter(models.Transaction.id == db_transaction.id).first()
        return db_transaction_with_asset
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction

def get_portfolios(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Portfolio).filter(models.Portfolio.owner_id == user_id).offset(skip).limit(limit).all()

def create_user_portfolio(db: Session, portfolio: schemas.PortfolioCreate, user_id: int):
    db_portfolio = models.Portfolio(**portfolio.model_dump(), owner_id=user_id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

def get_assets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Asset).offset(skip).limit(limit).all()

def get_asset_by_ticker(db: Session, ticker: str):
    return db.query(models.Asset).filter(models.Asset.ticker == ticker).first()

def create_asset(db: Session, asset: schemas.AssetCreate):
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset
