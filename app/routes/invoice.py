from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.invoice_service import InvoiceService
from app.schemas.invoice import InvoiceCreate, Invoice, InvoiceUpdate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("/", response_model=Invoice)
async def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    invoice.user_id = current_user.id
    return InvoiceService.create_invoice(db, invoice)


@router.get("/", response_model=List[Invoice])
async def list_invoices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    return InvoiceService.get_user_invoices(db, current_user.id, skip, limit)


@router.get("/{invoice_id}", response_model=Invoice)
async def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    invoice = InvoiceService.get_invoice(db, invoice_id)
    if invoice is None or invoice.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.put("/{invoice_id}", response_model=Invoice)
async def update_invoice(
    invoice_id: int,
    invoice_update: InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    db_invoice = InvoiceService.get_invoice(db, invoice_id)
    if db_invoice is None or db_invoice.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Invoice not found")

    for key, value in invoice_update.dict(exclude_unset=True).items():
        setattr(db_invoice, key, value)

    db.commit()
    db.refresh(db_invoice)
    return db_invoice


@router.delete("/{invoice_id}", status_code=204)
async def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    db_invoice = InvoiceService.get_invoice(db, invoice_id)
    if db_invoice is None or db_invoice.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.delete(db_invoice)
    db.commit()
