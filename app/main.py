from fastapi import FastAPI
from .database import engine, Base
from . import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Tracker API")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API and Database are running"}