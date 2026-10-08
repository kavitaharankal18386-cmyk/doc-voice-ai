from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import os
from twilio.rest import Client

from app.schemas import Appointment
from app.database import SessionLocal
from app.models import AppointmentDB

router = APIRouter()

# Twilio Credentials (Render Environment Variables madhe add kara)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "YOUR_TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "YOUR_TWILIO_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

def send_whatsapp_confirmation(phone_number: str, patient_name: str, appointment_time: str):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Phone number format fix (+91 formatting)
        clean_phone = phone_number.strip()
        if not clean_phone.startswith("+"):
            clean_phone = f"+91{clean_phone}"

        message_body = (
            f"Namaskar {patient_name}! 🩺\n\n"
            f"Tuzi appointment successfully book zali ahe.\n"
            f"📅 Time/Date: {appointment_time}\n\n"
            f"Kahi shanka aslyas ya number var sampark sadha. Dhanyavad!"
        )

        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=f"whatsapp:{clean_phone}"
        )
        print(f"WhatsApp sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"WhatsApp error: {str(e)}")


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
    # 1. Database madhe save kara
    new_appointment = AppointmentDB(
        patient_name=appointment.patient_name,
        phone_number=appointment.phone_number,
        appointment_time=appointment.appointment_time,
        call_id=appointment.call_id
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    # 2. WhatsApp Message Pathva
    send_whatsapp_confirmation(
        phone_number=appointment.phone_number,
        patient_name=appointment.patient_name,
        appointment_time=appointment.appointment_time
    )

    return {
        "success": True,
        "message": "Appointment saved and WhatsApp sent successfully!",
        "appointment_id": new_appointment.id
    }
    @router.get("/api/appointments")
def get_appointments(db: Session = Depends(get_db)):
    return db.query(AppointmentDB).all()