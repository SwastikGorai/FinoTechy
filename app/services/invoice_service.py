from sqlalchemy.orm import Session
from app.models.invoice import Invoice, InvoiceStatus
from app.schemas.invoice import InvoiceCreate
from datetime import datetime
import uuid


class InvoiceService:
    @staticmethod
    def generate_invoice_number():
        return f"INV-{uuid.uuid4().hex[:8].upper()}"

    @staticmethod
    def create_invoice(db: Session, invoice: InvoiceCreate):
        db_invoice = Invoice(
            **invoice.dict(),
            invoice_number=InvoiceService.generate_invoice_number()
        )
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)
        return db_invoice

    @staticmethod
    def get_invoice(db: Session, invoice_id: int):
        return db.query(Invoice).filter(Invoice.id == invoice_id).first()

    @staticmethod
    def get_user_invoices(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(Invoice).filter(Invoice.user_id == user_id)\
            .offset(skip).limit(limit).all()

    @staticmethod
    def update_invoice_status(db: Session, invoice_id: int, status: InvoiceStatus):
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if invoice:
            invoice.status = status
            invoice.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(invoice)
        return invoice
