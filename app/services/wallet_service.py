from sqlalchemy.orm import Session
from app.models.financial import Wallet, Transaction, TransactionType
from decimal import Decimal
from fastapi import HTTPException


class WalletService:
    @staticmethod
    def create_wallet(db: Session, user_id: int, currency: str):
        wallet = Wallet(
            user_id=user_id,
            currency=currency,
            balance=0.0
        )
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
        return wallet

    @staticmethod
    def get_user_wallets(db: Session, user_id: int):
        return db.query(Wallet).filter(Wallet.user_id == user_id).all()

    @staticmethod
    def get_wallet(db: Session, wallet_id: int, user_id: int):
        return db.query(Wallet).filter(
            Wallet.id == wallet_id,
            Wallet.user_id == user_id
        ).first()

    @staticmethod
    def add_transaction(
        db: Session,
        wallet_id: int,
        amount: Decimal,
        transaction_type: TransactionType,
        description: str
    ):
        wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        transaction = Transaction(
            wallet_id=wallet_id,
            amount=amount,
            type=transaction_type,
            description=description
        )
        db.add(transaction)

        if transaction_type == TransactionType.CREDIT:
            wallet.balance += amount
        else:
            if wallet.balance < amount:
                raise HTTPException(
                    status_code=400, detail="Insufficient funds")
            wallet.balance -= amount

        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def get_wallet_transactions(
        db: Session,
        wallet_id: int,
        skip: int = 0,
        limit: int = 100
    ):
        return db.query(Transaction)\
            .filter(Transaction.wallet_id == wallet_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
