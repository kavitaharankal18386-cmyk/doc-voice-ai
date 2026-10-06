import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.webhook import router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dr. Sharma's AI Receptionist",
    description="AI Receptionist API and Clinic Dashboard",
    version="1.0.0"
)

app.include_router(router)

if os.path.exists("frontend"):
    app.mount("/dashboard", StaticFiles(directory="frontend", html=True), name="frontend")