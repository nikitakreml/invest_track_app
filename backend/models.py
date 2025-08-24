from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    google_sheets_api_key = Column(String, nullable=True)
    google_sheets_spreadsheet_id = Column(String, nullable=True)
    tinkoff_invest_api_token = Column(String, nullable=True)
    auto_transaction_price_enabled = Column(Boolean, default=True)

    portfolios = relationship("Portfolio", back_populates="owner")

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="portfolios")
    transactions = relationship("Transaction", back_populates="portfolio")

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ticker = Column(String, unique=True, index=True)

    transactions = relationship("Transaction", back_populates="asset")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    type = Column(String)  # Buy/Sell
    price = Column(Float)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))

    asset = relationship("Asset", back_populates="transactions")
    portfolio = relationship("Portfolio", back_populates="transactions")
