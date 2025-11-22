import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_connection import SessionLocal
from models.user import User

def fix_admin():
    print("--- Admin Şifresi Düzeltiliyor ---")
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(email="admin@kuafor.com").first()
        if user:
            user.password_hash = "123"
            db.commit()
            print("BAŞARILI! Admin şifresi '123' olarak ayarlandı.")
        else:
            print("HATA: Admin bulunamadı.")
    except Exception as e:
        print(f"HATA: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_admin()