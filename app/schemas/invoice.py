from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from decimal import Decimal


class InvoiceBase(BaseModel):
    client_name: str
    client_email: EmailStr
    amount: Decimal
    currency: str
    due_date: datetime
    status: Optional[str] = "DRAFT"


class InvoiceCreate(InvoiceBase):
    user_id: int


class InvoiceUpdate(BaseModel):
    client_name: Optional[str] = None
    client_email: Optional[EmailStr] = None
    amount: Optional[Decimal] = None
    currency: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None


class Invoice(InvoiceBase):
    id: int
    invoice_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
