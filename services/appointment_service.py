from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from models.appointment import Appointment
from models.employee_availability import EmployeeAvailability
from models.salon_service import SalonService
from datetime import date, time, datetime, timedelta

def get_available_slots(db: Session, employee_id: int, check_date: date, duration_minutes: int) -> List[str]:
    """
    Belirtilen çalışanın, belirtilen tarihteki uygun saat aralıklarını hesaplar.
    """
    day_idx = check_date.weekday()
    
    availability = db.query(EmployeeAvailability).filter(
        and_(
            EmployeeAvailability.employee_id == employee_id,
            EmployeeAvailability.day_of_week == day_idx
        )
    ).first()

    if not availability:
        return []

    start_work = availability.start_time
    end_work = availability.end_time

    existing_apps = db.query(Appointment).filter(
        and_(
            Appointment.employee_id == employee_id,
            Appointment.appointment_date == check_date,
            Appointment.is_cancelled == False
        )
    ).all()

    busy_slots = []
    for app in existing_apps:
        busy_slots.append((app.start_time, app.end_time))

    available_slots = []
    
    current_dt = datetime.combine(check_date, start_work)
    end_dt = datetime.combine(check_date, end_work)
    
    while current_dt + timedelta(minutes=duration_minutes) <= end_dt:
        slot_start = current_dt.time()
        slot_end = (current_dt + timedelta(minutes=duration_minutes)).time()

        is_clash = False
        for busy_start, busy_end in busy_slots:
            if slot_start < busy_end and slot_end > busy_start:
                is_clash = True
                break
        
        if not is_clash:
            available_slots.append(f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}")
        
        current_dt += timedelta(minutes=30) 

    return available_slots

def create_appointment(db: Session, user_id: int, salon_id: int, employee_id: int, salon_service_id: int, app_date: date, start_time_str: str):
    h, m = map(int, start_time_str.split(':'))
    start_time = time(h, m)
    
    service = db.query(SalonService).filter(SalonService.id == salon_service_id).first()
    duration = service.duration_minutes if service else 30
    
    dummy_date = datetime.combine(date.today(), start_time)
    end_time = (dummy_date + timedelta(minutes=duration)).time()

    new_app = Appointment(
        user_id=user_id,
        salon_id=salon_id,
        employee_id=employee_id,
        salon_service_id=salon_service_id,
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
        joinedload(Appointment.salon_service).joinedload(SalonService.service)
    ).all()