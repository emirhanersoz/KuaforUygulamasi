from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database.db_connection import Base
class SalonService(Base):
    __tablename__ = "salon_services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    salon_id = Column(Integer, ForeignKey('salons.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    price_tl = Column(DECIMAL(10, 2), nullable=False)

    salon = relationship("Salon", back_populates="salon_services")
    service = relationship("Service", back_populates="salon_services")

    __table_args__ = (
        UniqueConstraint('salon_id', 'service_id', name='uq_salon_service'),
    )
    
    def __repr__(self):
        return f"<SalonService(salon_id={self.salon_id}, price={self.price_tl})>"