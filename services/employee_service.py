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

def add_new_employee(db: Session, first_name: str, last_name: str, email: str, password: str, salon_id: int, role_name: str) -> Optional[Employee]:
    """Yeni bir çalışan oluşturur (Önce User, sonra Employee tablosuna ekler)."""
    user = create_user(db, first_name, last_name, email, password, role_name)
    
    if not user:
        return None
    
    is_admin = (role_name == "Yönetici")
    
    new_employee = Employee(user_id=user.id, salon_id=salon_id, is_admin=is_admin)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

def get_all_employees(db: Session) -> List[Employee]:
    """Tüm çalışanları getirir."""
    return db.query(Employee).options(joinedload(Employee.user), joinedload(Employee.salon)).all()

def get_employees_by_salon(db: Session, salon_id: int) -> List[Employee]:
    """Bir salondaki çalışanları getirir."""
    return db.query(Employee).filter(Employee.salon_id == salon_id).options(joinedload(Employee.user)).all()

def get_services_for_employee(db: Session, employee_id: int, salon_id: int):
    """
    Bir çalışanın verebildiği hizmetleri (Fiyat ve Süreleriyle) getirir.
    Artık salon_id'ye bakmıyoruz, direkt çalışanın yeteneklerine bakıyoruz.
    Ancak parametre uyumu için salon_id'yi tutuyoruz (kullanılmayabilir).
    """
    services = db.query(EmployeeService).options(joinedload(EmployeeService.service))\
        .filter(EmployeeService.employee_id == employee_id)\
        .all()
    return services

def set_employee_availability(db: Session, employee_id: int, day_of_week: int, start: time, end: time):
    """Çalışanın belirli bir gündeki mesai saatini ayarlar/günceller."""
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

def get_employee_appointments(db: Session, employee_id: int):
    """Çalışana gelen tüm randevuları getirir."""
    return db.query(Appointment).options(
        joinedload(Appointment.user),
        joinedload(Appointment.service) 
    ).filter(Appointment.employee_id == employee_id).order_by(Appointment.appointment_date, Appointment.start_time).all()

def update_appointment_status(db: Session, appointment_id: int, is_confirmed: bool):
    """Randevuyu onaylar veya reddeder."""
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
    """Çalışana özel fiyatla yeni bir hizmet tanımlar."""
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