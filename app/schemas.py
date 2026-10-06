from pydantic import BaseModel
from typing import Optional

class Appointment(BaseModel):
    patient_name: str
    phone_number: str
    appointment_time: str
    call_id: Optional[str] = None

class SendOTP(BaseModel):
    phone_number: str

class VerifyOTP(BaseModel):
    phone_number: str
    otp: str

class ShopRegister(BaseModel):
    shop_name: str
    owner_name: str
    phone_number: str
    category: str