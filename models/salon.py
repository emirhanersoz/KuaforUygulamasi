from sqlalchemy import Column, Integer, String, Text, Boolean, Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db_connection import Base

class Salon(Base):
    __tablename__ = "salons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(Text)
    phone_number = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(Time, default=func.now())

    employees = relationship("Employee", back_populates="salon")
    salon_services = relationship("SalonService", back_populates="salon")
    appointments = relationship("Appointment", back_populates="salon")

    def __repr__(self):
        return f"<Salon(name='{self.name}', address='{self.address}')>"