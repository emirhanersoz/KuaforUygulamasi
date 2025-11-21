from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from config import DB_CONFIG

DB_URL = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"

# Oluşturduğumuz URL stringini motoru yaratırken kullanıyoruz.
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

try:
    from models import Role, User, Salon, Employee, Service, SalonService, EmployeeService, Appointment, EmployeeAvailability
except ImportError:
    pass
# ---------------------------------------------------------------------------

def get_db():
    """
    Veritabanı oturumu (session) sağlayan generator fonksiyon.
    İşlem bittiğinde oturumu otomatik olarak kapatır.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Veritabanı tablolarını oluşturur."""
    Base.metadata.create_all(bind=engine)
    print("Tablolar başarıyla oluşturuldu (veya zaten vardı).")

if __name__ == '__main__':
    create_tables()