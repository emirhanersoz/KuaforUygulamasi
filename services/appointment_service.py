from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from models.appointment import Appointment
from datetime import date, time

def create_appointment(db: Session, user_id: int, salon_id: int, employee_id: int, service_id: int, app_date: date, start_time: time, end_time: time):
    new_app = Appointment(
        user_id=user_id,
        salon_id=salon_id,
        employee_id=employee_id,
        salon_service_id=service_id,
        appointment_date=app_date,
        start_time=start_time,
        end_time=end_time,
        is_confirmed=True 
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

def get_all_appointments(db: Session):
    return db.query(Appointment).options(
        joinedload(Appointment.user),
        joinedload(Appointment.employee),
        joinedload(Appointment.salon_service).joinedload(object.service)
    ).all()