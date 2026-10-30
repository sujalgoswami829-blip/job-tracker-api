from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI
from .database import engine
from . import models
from .routers import auth, jobs

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Tracker API")

app.include_router(auth.router)
app.include_router(jobs.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API and Database are running"}
@app.get("/")
def serve_homepage():
    return FileResponse("app/index.html")