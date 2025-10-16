from sqlalchemy import Column, Integer, TIME, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from database.db_connection import Base

class EmployeeAvailability(Base):
    __tablename__ = "employee_availability"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)

    day_of_week = Column(Integer, nullable=False)
    start_time = Column(TIME, nullable=False)
    end_time = Column(TIME, nullable=False)

    employee = relationship("Employee", back_populates="availability")

    __table_args__ = (
        UniqueConstraint('employee_id', 'day_of_week', name='uq_employee_day'),
        CheckConstraint('day_of_week >= 0 AND day_of_week <= 6', name='cc_day_of_week')
    )

    def __repr__(self):
        return f"<EmployeeAvailability(employee_id={self.employee_id}, day_of_week={self.day_of_week})>"