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

class TransactionBase(BaseModel):
    date: date
    type: str
    price: float
    asset_id: int
    portfolio_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True
