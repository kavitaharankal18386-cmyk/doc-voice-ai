from sqlalchemy import Column, Integer, String
from app.database import Base

class AppointmentDB(Base):
    _tablename_ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    appointment_time = Column(String, nullable=False)
    call_id = Column(String, nullable=True)
    status = Column(String, default="scheduled")