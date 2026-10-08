import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Database and Webhook imports with fallback handling
try:
    from app.webhook import router as webhook_router
    from app.database import Base, engine
except ModuleNotFoundError:
    from webhook import router as webhook_router
    from database import Base, engine

# Database tables create kara
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dr. Sharma's AI Receptionist",
    description="AI Receptionist API and Clinic Dashboard",
    version="1.0.0"
)

# CORS Middleware enable kara
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Webhook Router include kara
app.include_router(webhook_router)

# Frontend Dashboard mount kara
if os.path.exists("frontend"):
    app.mount("/dashboard", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def home():
    return {"status": "Doc Voice AI Backend Running"}