from sqlalchemy import Column, Integer, String
from database.base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role(role_name='{self.role_name}')>"