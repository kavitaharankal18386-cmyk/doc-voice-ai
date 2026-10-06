from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import Appointment, SendOTP, VerifyOTP, ShopRegister
from app.database import SessionLocal
from app.models import AppointmentDB

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/webhook/appointment")
def receive_appointment(
    appointment: Appointment,
    db: Session = Depends(get_db)
):
    new_appointment = AppointmentDB(
        patient_name=appointment.patient_name,
        phone_number=appointment.phone_number,
        appointment_time=appointment.appointment_time,
        call_id=appointment.call_id
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return {
        "success": True,
        "message": "Appointment saved successfully",
        "appointment_id": new_appointment.id
    }

@router.post("/api/send-otp")
def send_otp(data: SendOTP):
    return {
        "success": True,
        "message": f"OTP sent successfully to {data.phone_number}",
        "otp_test": "123456"
    }

@router.post("/api/verify-otp")
def verify_otp(data: VerifyOTP):
    if data.otp == "123456":
        return {"success": True, "message": "Mobile number verified successfully!"}
    return {"success": False, "message": "Invalid OTP. Try again."}