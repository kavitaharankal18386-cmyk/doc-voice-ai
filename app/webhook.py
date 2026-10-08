import os
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from twilio.rest import Client
from database import get_db, AppointmentDB

router = APIRouter()

# Twilio Credentials (Environment Variables kinva Direct Hardcode)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "YOUR_TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "YOUR_TWILIO_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Standard Twilio Sandbox Number

def send_whatsapp_confirmation(to_number: str, patient_name: str, appointment_time: str):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Phone number WhatsApp format madhe convert kara
        formatted_number = to_number if to_number.startswith("whatsapp:") else f"whatsapp:{to_number}"
        
        message_body = (
            f"Namaskar {patient_name}! 🩺\n"
            f"Tumchi appointment yashasviritya book jhali ahe.\n\n"
            f"📅 Date/Time: {appointment_time}\n"
            f"📍 Location: Clinic\n\n"
            f"Dhanyavaad!"
        )
        
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=formatted_number
        )
        print(f"WhatsApp sent! SID: {message.sid}")
    except Exception as e:
        print(f"Error sending WhatsApp: {e}")

@router.post("/webhook/appointment")
async def handle_appointment(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        print("Received Webhook Data:", data)
        
        # Bolna AI kaddun yenara JSON payload extract kara
        patient_name = data.get("patient_name", "Patient")
        phone_number = data.get("phone_number", "")
        appointment_time = data.get("appointment_time", "Today")
        
        # Database madhe record save kara
        new_appointment = AppointmentDB(
            patient_name=patient_name,
            phone_number=phone_number,
            appointment_time=appointment_time
        )
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        
        # WhatsApp Message Pathva
        if phone_number:
            send_whatsapp_confirmation(
                to_number=phone_number,
                patient_name=patient_name,
                appointment_time=appointment_time
            )
            
        return {
            "success": True,
            "message": "Appointment saved and WhatsApp sent successfully!",
            "appointment_id": new_appointment.id
        }
    except Exception as e:
        print("Error in webhook:", str(e))
        return {"success": False, "error": str(e)}

@router.get("/api/appointments")
def get_appointments(db: Session = Depends(get_db)):
    return db.query(AppointmentDB).all()