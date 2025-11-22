from sqlalchemy.orm import Session, joinedload
from typing import Optional
from models.user import User
from models.role import Role

def hash_password(password: str) -> str:
    return password

def check_password(provided_password: str, stored_password_hash: str) -> bool:
    print(f"DEBUG: Şifre kontrol ediliyor... Girilen: {provided_password} | Kayıtlı: {stored_password_hash}")
    return provided_password == stored_password_hash

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    print(f"DEBUG: DB sorgusu yapılıyor -> {email}")
    try:
        user = db.query(User).options(joinedload(User.role)).filter_by(email=email).first()
        
        if not user:
            print("DEBUG: Kullanıcı veritabanında bulunamadı.")
            return None

        print(f"DEBUG: Kullanıcı bulundu: {user.first_name}, Şifre kontrolüne geçiliyor...")
        if check_password(password, user.password_hash):
            print("DEBUG: Şifre DOĞRU.")
            return user
        else:
            print("DEBUG: Şifre YANLIŞ.")
            return None
    except Exception as e:
        print(f"DEBUG HATASI (authenticate_user): {e}")
        return None

def create_user(db: Session, first_name: str, last_name: str, email: str, password: str, role_name: str):
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
        role_id=role.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user