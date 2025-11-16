import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import bcrypt
import config
from typing import Optional
from sqlalchemy.orm import Session, sessionmaker, joinedload
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import urllib.parse as up

from models.user import User
from models.role import Role

try:
    from database.db_connection import get_db
except ImportError:
    try:
        from database.db_connection import SessionLocal
        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
    except Exception:
        if getattr(config, 'DATABASE_URL', None):
            engine = create_engine(config.DATABASE_URL)
            SessionLocalFallback = sessionmaker(bind=engine)
            def get_db():
                db = SessionLocalFallback()
                try:
                    yield db
                finally:
                    db.close()
        else:
            def get_db():
                raise ImportError(
                    "database.db_connection does not export 'get_db' or 'SessionLocal', and config.DATABASE_URL is not set. "
                    "Provide one of these so user_service can create sessions."
                )

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(provided_password: str, stored_password_hash: str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password_hash.encode('utf-8'))

def create_user(
    db: Session, 
    first_name: str, 
    last_name: str, 
    email: str, 
    password: str, 
    role_name: str
) -> Optional[User]:
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
    user = db.query(User).options(joinedload(User.role)).filter_by(email=email).first()
    if user and check_password(password, user.password_hash):
        try:
            if getattr(user, 'role', None) is not None:
                try:
                    db.expunge(user.role)
                except Exception:
                    pass
            db.expunge(user)
        except Exception:
            pass
        return user
    return None

if __name__ == '__main__':
    try:
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
    except ProgrammingError as e:
        print("Veritabanı bağlantısı hatası:", e)
        print("Muhtemelen hedef veritabanı ('kuafor') mevcut değil veya DATABASE_URL hatalı.")
        try:
            msg = str(e)
            if 'Unknown database' in msg or '1049' in msg:
                try:
                    from database import db_connection as db_conn
                except Exception:
                    db_conn = None

                db_url = None
                if db_conn is not None:
                    db_url = getattr(db_conn, 'DATABASE_URL', None)
                    if not db_url:
                        engine_obj = getattr(db_conn, 'engine', None)
                        if engine_obj is not None:
                            db_url = str(engine_obj.url)

                if not db_url:
                    db_url = getattr(config, 'DATABASE_URL', None)

                if not db_url:
                    raise RuntimeError("DATABASE_URL veya engine bulunamadı; otomatik oluşturma için bağlantı bilgisi gerekli.")

                parsed = up.urlparse(db_url)
                dbname = parsed.path.lstrip('/')
                if not dbname:
                    raise RuntimeError("URL içinde veritabanı adı bulunamadı.")

                server_parsed = parsed._replace(path='', params='', query='', fragment='')
                server_url = server_parsed.geturl()

                admin_engine = create_engine(server_url)
                with admin_engine.connect() as conn:
                    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{dbname}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"))
                print(f"Veritabanı '{dbname}' başarıyla oluşturuldu veya zaten mevcut. Lütfen komutu tekrar çalıştırın.")
                sys.exit(0)
        except Exception as ex:
            print("Otomatik veritabanı oluşturulamadı:", ex)
            print("Çözüm önerileri:")
            print(" - MySQL sunucusunda 'kuafor' veritabanını oluşturun veya")
            print(" - proje yapılandırmasındaki bağlantı dizesini (DATABASE_URL) uygun bir veritabanına işaret edecek şekilde güncelleyin.")
    except Exception as e:
        print("Beklenmeyen hata:", e)