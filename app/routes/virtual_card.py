from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.virtual_card_service import VirtualCardService
from app.services.auth_service import AuthService
from app.schemas.financial import VirtualCard

router = APIRouter(prefix="/virtual-cards", tags=["virtual-cards"])


@router.post("/", response_model=VirtualCard)
async def create_virtual_card(
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    return VirtualCardService.create_virtual_card(db, current_user.id)


@router.get("/", response_model=List[VirtualCard])
async def list_virtual_cards(
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    return VirtualCardService.get_user_cards(db, current_user.id)


@router.post("/{card_id}/deactivate", response_model=VirtualCard)
async def deactivate_virtual_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(AuthService.get_current_user)
):
    card = VirtualCardService.deactivate_card(db, card_id, current_user.id)
    if not card:
        raise HTTPException(status_code=404, detail="Virtual card not found")
    return card
