from typing import List, Optional
from sqlalchemy.orm import Session
from models.salon import Salon

def create_salon(db: Session, name: str, address: str, phone: str) -> Salon:
    new_salon = Salon(name=name, address=address, phone_number=phone)
    db.add(new_salon)
    db.commit()
    db.refresh(new_salon)
    return new_salon

def get_all_salons(db: Session) -> List[Salon]:
    return db.query(Salon).filter(Salon.is_active == True).all()

def get_salon_by_id(db: Session, salon_id: int) -> Optional[Salon]:
    return db.query(Salon).filter(Salon.id == salon_id).first()

def update_salon(db: Session, salon_id: int, name: str, address: str, phone: str) -> bool:
    salon = db.query(Salon).filter(Salon.id == salon_id).first()
    if salon:
        salon.name = name
        salon.address = address
        salon.phone_number = phone
        db.commit()
        return True
    return False

def delete_salon(db: Session, salon_id: int) -> bool:
    salon = get_salon_by_id(db, salon_id)
    if salon:
        salon.is_active = False
        db.commit()
        return True
    return False
