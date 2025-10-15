import bcrypt
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.user import User
from models.role import Role
from database.db_connection import get_db

def hash_password(password: str) -> str:
    """Hashes a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(provided_password: str, stored_password_hash: str) -> bool:
    """Verifies a provided password against a stored hashed password."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password_hash.encode('utf-8'))

def create_user(
    db: Session, 
    first_name: str, 
    last_name: str, 
    email: str, 
    password: str, 
    role_name: str
) -> Optional[User]:
    """
    Creates a new user and adds them to the database.
    Returns None if a user with the given email already exists.
    """
    hashed_pass = hash_password(password)
    
    role = db.query(Role).filter_by(role_name=role_name).first()
    if not role:
        if role_name in ["Yönetici", "Çalışan", "Müşteri"]:
            role = Role(role_name=role_name)
            db.add(role)
            db.commit()
            db.refresh(role)
        else:
            print(f"Hata: Geçersiz rol adı '{role_name}'.")
            return None
        
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=hashed_pass,
        role_id=role.id
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        return None

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter_by(email=email).first()
    if user and check_password(password, user.password_hash):
        return user
    return None

if __name__ == '__main__':
    # Test code
    for db in get_db():
        print("Kullanıcı oluşturma testi...")
        
        new_admin = create_user(db, "Admin", "User", "admin@kuafor.com", "admin123", "Yönetici")
        if new_admin:
            print(f"'{new_admin.email}' adresi ile kullanıcı başarıyla oluşturuldu.")
        else:
            print("Kullanıcı oluşturma başarısız. Muhtemelen e-posta zaten mevcut.")
            
    for db in get_db():
        print("\nKullanıcı doğrulama testi...")

        authenticated_user = authenticate_user(db, "admin@kuafor.com", "admin123")
        if authenticated_user:
            print(f"'{authenticated_user.email}' adresi ile giriş başarılı. Rolü: {authenticated_user.role.role_name}")
        else:
            print("Giriş bilgileri yanlış.")