from sqlalchemy import Column, Integer, DATE, TIME, Boolean, ForeignKey, UniqueConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db_connection import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    salon_id = Column(Integer, ForeignKey('salons.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    salon_service_id = Column(Integer, ForeignKey('salon_services.id'), nullable=False)
    
    appointment_date = Column(DATE, nullable=False)
    start_time = Column(TIME, nullable=False)
    end_time = Column(TIME, nullable=False)
    
    is_confirmed = Column(Boolean, default=False)
    is_cancelled = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=func.now())

    user = relationship("User", backref="appointments")
    salon = relationship("Salon", back_populates="appointments")
    employee = relationship("Employee", back_populates="appointments")
    salon_service = relationship("SalonService", backref="appointments")

    __table_args__ = (
        UniqueConstraint('employee_id', 'appointment_date', 'start_time', name='uq_employee_datetime'),
    )

    def __repr__(self):
        return f"<Appointment(date={self.appointment_date}, employee_id={self.employee_id})>"