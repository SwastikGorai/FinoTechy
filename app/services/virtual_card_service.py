from sqlalchemy.orm import Session
from app.models.financial import VirtualCard
from datetime import datetime, timedelta
import random
import string


class VirtualCardService:
    @staticmethod
    def generate_card_number():
        return ''.join(random.choices(string.digits, k=16))

    @staticmethod
    def generate_cvv():
        return ''.join(random.choices(string.digits, k=3))

    @staticmethod
    def generate_expiry_date():
        expiry_date = datetime.now() + timedelta(days=365)
        return expiry_date.strftime("%m/%y")

    @staticmethod
    def create_virtual_card(db: Session, user_id: int):
        virtual_card = VirtualCard(
            user_id=user_id,
            card_number=VirtualCardService.generate_card_number(),
            expiry_date=VirtualCardService.generate_expiry_date(),
            cvv=VirtualCardService.generate_cvv(),
            is_active=True
        )
        db.add(virtual_card)
        db.commit()
        db.refresh(virtual_card)
        return virtual_card

    @staticmethod
    def get_user_cards(db: Session, user_id: int):
        return db.query(VirtualCard).filter(
            VirtualCard.user_id == user_id,
            VirtualCard.is_active == True # noqa
        ).all()

    @staticmethod
    def deactivate_card(db: Session, card_id: int, user_id: int):
        card = db.query(VirtualCard).filter(
            VirtualCard.id == card_id,
            VirtualCard.user_id == user_id
        ).first()
        if card:
            card.is_active = False
            db.commit()
            db.refresh(card)
        return card
