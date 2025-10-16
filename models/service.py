from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database.db_connection import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)

    salon_services = relationship("SalonService", back_populates="service")
    employee_services = relationship("EmployeeService", back_populates="service")

    def __repr__(self):
        return f"<Service(name='{self.service_name}')>"