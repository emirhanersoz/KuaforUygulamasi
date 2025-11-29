from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from database.base import Base

engine = create_engine(DATABASE_URL, connect_args={'connect_timeout': 5})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    try:
        from models.role import Role
        from models.user import User
        from models.salon import Salon
        from models.employee import Employee
        from models.service import Service
        from models.salon_service import SalonService
        from models.employee_service import EmployeeService
        from models.appointment import Appointment
        from models.employee_availability import EmployeeAvailability
    except ImportError as e:
        print(f"Model import hatası: {e}")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("Tablolar başarıyla oluşturuldu.")
    except Exception as e:
        print(f"Tablo oluşturma hatası (Bağlantı Sorunu): {e}")

if __name__ == '__main__':
    create_tables()