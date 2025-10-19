from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.db_connection import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)

    salon_id = Column(Integer, ForeignKey('salons.id'))
    
    is_admin = Column(Boolean, default=False)

    user = relationship("User", backref="employee", uselist=False)
    salon = relationship("Salon", back_populates="employees")
    employee_services = relationship("EmployeeService", back_populates="employee")
    availability = relationship("EmployeeAvailability", back_populates="employee")
    appointments = relationship("Appointment", back_populates="employee")

    def __repr__(self):
        return f"<Employee(user_id={self.user_id}, salon_id={self.salon_id})>"