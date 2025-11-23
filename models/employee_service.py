from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from database.base import Base

class EmployeeService(Base):
    __tablename__ = "employee_services"

    employee_id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    service_id = Column(Integer, ForeignKey('services.id'), primary_key=True)
    
    duration_minutes = Column(Integer, nullable=False, default=30)
    price_tl = Column(DECIMAL(10, 2), nullable=False, default=100.00)

    employee = relationship("Employee", back_populates="employee_services")
    service = relationship("Service", back_populates="employee_services")

    def __repr__(self):
        return f"<EmployeeService(emp={self.employee_id}, srv={self.service_id}, price={self.price_tl})>"