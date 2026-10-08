import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
import app.models  # Models import karne aavashyak ahe!
from app.webhook import router as webhook_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Doc Voice AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router)

if os.path.exists("frontend"):
    app.mount("/dashboard", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def home():
    return {"status": "Doc Voice AI Backend Running"}