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

def create_user(db: Session, first_name: str, last_name: str, email: str, password: str, role_name: str, phone: str = ""):
    role = db.query(Role).filter_by(role_name=role_name).first()
    if not role:
        role = Role(role_name=role_name)
        db.add(role)
        db.commit()
        db.refresh(role)
        
    hashed = hash_password(password)
    
    new_user = User(
        first_name=first_name, 
        last_name=last_name, 
        email=email, 
        password_hash=hashed, 
        role_id=role.id,
        phone_number=phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session) -> List[User]:
    """Tüm kullanıcıları (Rolleri ile birlikte) getirir."""
    return db.query(User).options(joinedload(User.role)).all()

def delete_user(db: Session, user_id: int) -> bool:
    """ID'si verilen kullanıcıyı siler."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def update_user_role(db: Session, user_id: int, new_role_name: str) -> bool:
    """Kullanıcının rolünü değiştirir."""
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter_by(role_name=new_role_name).first()
    
    if user and role:
        user.role_id = role.id
        db.commit()
        return True
    return False