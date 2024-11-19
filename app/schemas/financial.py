from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class WalletBase(BaseModel):
    currency: str


class WalletCreate(WalletBase):
    pass


class Wallet(WalletBase):
    id: int
    user_id: int
    balance: Decimal
    created_at: datetime

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    amount: Decimal
    type: str
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    wallet_id: int


class Transaction(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True



class VirtualCardBase(BaseModel):
    card_number: str
    expiry_date: str
    cvv: str
    
class VirtualCardCreate(VirtualCardBase):
    pass

class VirtualCard(VirtualCardBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
        
