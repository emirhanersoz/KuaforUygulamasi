from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models.user import User
from models.role import Role

def hash_password(password: str) -> str:
    return password

def check_password(provided_password: str, stored_password_hash: str) -> bool:
    return provided_password == stored_password_hash

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    try:
        user = db.query(User).options(joinedload(User.role)).filter_by(email=email).first()
        if user and check_password(password, user.password_hash):
            return user
        return None
    except Exception as e:
        print(f"Auth Hatası: {e}")
        return None

def create_user(db: Session, first_name: str, last_name: str, email: str, password: str, role_id: int, phone: str = ""):
    hashed = hash_password(password)
    
    new_user = User(
        first_name=first_name, 
        last_name=last_name, 
        email=email, 
        password_hash=hashed, 
        role_id=role_id,
        phone_number=phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session) -> List[User]:
    return db.query(User).options(joinedload(User.role)).all()

def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def update_user_role(db: Session, user_id: int, new_role_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.role_id = new_role_id
        db.commit()
        return True
    return False

def update_user_details(db: Session, user_id: int, first_name: str, last_name: str, email: str, phone: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone
        db.commit()
        return True
    return False