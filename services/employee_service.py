from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from datetime import time

from models.employee import Employee
from models.user import User
from models.appointment import Appointment
from models.employee_availability import EmployeeAvailability
from models.employee_service import EmployeeService
from models.service import Service
from services.user_service import create_user

def add_new_employee(db: Session, first_name: str, last_name: str, email: str, password: str, salon_id: int, role_id: int) -> Optional[Employee]:
    user = create_user(db, first_name, last_name, email, password, role_id)
    
    if not user:
        return None
    
    is_admin = (role_id == 3)
    
    new_employee = Employee(user_id=user.id, salon_id=salon_id, is_admin=is_admin)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

def get_all_employees(db: Session) -> List[Employee]:
    return db.query(Employee).options(joinedload(Employee.user), joinedload(Employee.salon)).all()

def get_employees_by_salon(db: Session, salon_id: int) -> List[Employee]:
    return db.query(Employee).filter(Employee.salon_id == salon_id).options(joinedload(Employee.user)).all()

def update_employee(db: Session, emp_id: int, first_name: str, last_name: str, email: str, salon_id: int, role_id: int) -> bool:
    emp = db.query(Employee).options(joinedload(Employee.user)).filter(Employee.id == emp_id).first()
    
    if emp and emp.user:
        emp.user.first_name = first_name
        emp.user.last_name = last_name
        emp.user.email = email
        emp.user.role_id = role_id
        
        emp.salon_id = salon_id
        emp.is_admin = (role_id == 3)
        
        db.commit()
        return True
    return False

def get_services_for_employee(db: Session, employee_id: int, salon_id: int):
    services = db.query(EmployeeService).options(joinedload(EmployeeService.service))\
        .filter(EmployeeService.employee_id == employee_id)\
        .all()
    return services

def set_employee_availability(db: Session, employee_id: int, day_of_week: int, start: time, end: time):
    availability = db.query(EmployeeAvailability).filter(
        and_(
            EmployeeAvailability.employee_id == employee_id,
            EmployeeAvailability.day_of_week == day_of_week
        )
    ).first()

    if availability:
        availability.start_time = start
        availability.end_time = end
    else:
        new_av = EmployeeAvailability(
            employee_id=employee_id,
            day_of_week=day_of_week,
            start_time=start,
            end_time=end
        )
        db.add(new_av)
    db.commit()

def get_employee_availability_list(db: Session, employee_id: int):
    return db.query(EmployeeAvailability).filter(
        EmployeeAvailability.employee_id == employee_id
    ).order_by(EmployeeAvailability.day_of_week).all()

def get_employee_appointments(db: Session, employee_id: int):
    return db.query(Appointment).options(
        joinedload(Appointment.user),
        joinedload(Appointment.service) 
    ).filter(Appointment.employee_id == employee_id).order_by(Appointment.appointment_date, Appointment.start_time).all()

def update_appointment_status(db: Session, appointment_id: int, is_confirmed: bool):
    app = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if app:
        app.is_confirmed = is_confirmed
        if not is_confirmed:
            app.is_cancelled = True
        else:
            app.is_cancelled = False
        db.commit()
        return True
    return False

def add_service_to_employee(db: Session, employee_id: int, service_name: str, duration: int, price: float):
    service = db.query(Service).filter(Service.service_name == service_name).first()
    if not service:
        service = Service(service_name=service_name, description="Oto-oluşturuldu")
        db.add(service)
        db.commit()
        db.refresh(service)
    
    emp_service = db.query(EmployeeService).filter(
        and_(EmployeeService.employee_id == employee_id, EmployeeService.service_id == service.id)
    ).first()

    if emp_service:
        emp_service.duration_minutes = duration
        emp_service.price_tl = price
    else:
        emp_service = EmployeeService(
            employee_id=employee_id,
            service_id=service.id,
            duration_minutes=duration,
            price_tl=price
        )
        db.add(emp_service)
    db.commit()