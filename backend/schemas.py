from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    google_sheets_api_key: Optional[str] = None

    class Config:
        from_attributes = True

class PortfolioBase(BaseModel):
    name: str

class PortfolioCreate(PortfolioBase):
    pass

class Portfolio(PortfolioBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

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
