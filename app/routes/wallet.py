from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.wallet_service import WalletService
from app.services.auth_service import AuthService
from app.schemas.financial import WalletCreate, Wallet, Transaction
from app.models.financial import TransactionType
from decimal import Decimal

router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.post("/", response_model=Wallet)
async def create_wallet(
    wallet: WalletCreate,
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    return WalletService.create_wallet(db, current_user.id, wallet.currency)


@router.get("/", response_model=List[Wallet])
async def list_wallets(
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    return WalletService.get_user_wallets(db, current_user.id)


@router.post("/{wallet_id}/deposit", response_model=Transaction)
async def deposit_funds(
    wallet_id: int,
    amount: Decimal,
    description: str,
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    wallet = WalletService.get_wallet(db, wallet_id, current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return WalletService.add_transaction(
        db,
        wallet_id,
        amount,
        TransactionType.CREDIT,
        description
    )


@router.post("/{wallet_id}/withdraw", response_model=Transaction)
async def withdraw_funds(
    wallet_id: int,
    amount: Decimal,
    description: str,
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    wallet = WalletService.get_wallet(db, wallet_id, current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return WalletService.add_transaction(
        db,
        wallet_id,
        amount,
        TransactionType.DEBIT,
        description
    )


@router.get("/{wallet_id}/transactions", response_model=List[Transaction])
async def get_wallet_transactions(
    wallet_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    wallet = WalletService.get_wallet(db, wallet_id, current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return WalletService.get_wallet_transactions(db, wallet_id, skip, limit)
