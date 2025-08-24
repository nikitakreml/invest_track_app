from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class PortfolioBase(BaseModel):
    name: str

class PortfolioCreate(PortfolioBase):
    pass

class Portfolio(PortfolioBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    portfolios: List[Portfolio] = []
    google_sheets_api_key: Optional[str] = None
    google_sheets_spreadsheet_id: Optional[str] = None
    tinkoff_invest_api_token: Optional[str] = None
    auto_transaction_price_enabled: bool = True
    balance: float # Add balance to the User schema

    class Config:
        from_attributes = True

class UserSettings(BaseModel):
    google_sheets_api_key: Optional[str] = None
    google_sheets_spreadsheet_id: Optional[str] = None
    tinkoff_invest_api_token: Optional[str] = None
    auto_transaction_price_enabled: Optional[bool] = None
    balance: Optional[float] = None # Allow balance to be updated via settings

class AssetBase(BaseModel):
    name: str
    ticker: str

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: int

    class Config:
        from_attributes = True

# Base transaction fields shared across response models
class TransactionBase(BaseModel):
    date: date
    type: str
    price: float

# Create schema accepts asset_name from client
class TransactionCreate(TransactionBase):
    asset_name: str

# Response schema returns nested asset instead of asset_name
class Transaction(TransactionBase):
    id: int
    portfolio_id: int
    asset: Asset

    class Config:
        from_attributes = True

class GoogleSheetsApiKey(BaseModel):
    api_key: str

class TopUpWithdrawRequest(BaseModel):
    amount: float # Schema for top-up/withdraw requests
