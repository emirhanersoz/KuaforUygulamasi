from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.db_connection import Base

class EmployeeService(Base):
    __tablename__ = "employee_services"

    employee_id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    service_id = Column(Integer, ForeignKey('services.id'), primary_key=True)

    employee = relationship("Employee", back_populates="employee_services")
    service = relationship("Service", back_populates="employee_services")

    def __repr__(self):
        return f"<EmployeeService(employee_id={self.employee_id}, service_id={self.service_id})>"