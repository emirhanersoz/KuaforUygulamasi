from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from models.employee import Employee
from models.user import User
from services.user_service import create_user

def add_new_employee(db: Session, first_name: str, last_name: str, email: str, password: str, salon_id: int, role_name: str) -> Optional[Employee]:
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
    return db.query(Employee).options(joinedload(Employee.user), joinedload(Employee.salon)).all()

def get_employees_by_salon(db: Session, salon_id: int) -> List[Employee]:
    return db.query(Employee).filter(Employee.salon_id == salon_id).options(joinedload(Employee.user)).all()