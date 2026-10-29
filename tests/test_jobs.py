import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import models

# 1. Create a separate test database (SQLite in memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# 2. Override the real database with the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Variables to store test data
test_user = {"email": "pytest@test.com", "password": "password123"}
access_token = ""
job_id = None

# --- TESTS START HERE ---

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_register_user():
    response = client.post("/register", json=test_user)
    assert response.status_code == 200
    assert response.json()["email"] == "pytest@test.com"

def test_register_duplicate_user():
    response = client.post("/register", json=test_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_user():
    global access_token
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]

def test_login_wrong_password():
    response = client.post("/login", data={"username": test_user["email"], "password": "wrongpassword"})
    assert response.status_code == 403

def test_create_job():
    global job_id
    headers = {"Authorization": f"Bearer {access_token}"}
    job_data = {"company": "Google", "role": "Software Engineer", "status": "Applied"}
    response = client.post("/jobs/", json=job_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["company"] == "Google"
    job_id = response.json()["id"]

def test_get_jobs():
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/jobs/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_filter_jobs():
    headers = {"Authorization": f"Bearer {access_token}"}
    # Test status filter
    response = client.get("/jobs/?status=Applied", headers=headers)
    assert len(response.json()) == 1
    # Test company search
    response = client.get("/jobs/?company=Google", headers=headers)
    assert len(response.json()) == 1

def test_update_job():
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put(f"/jobs/{job_id}", json={"status": "Interview"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "Interview"

def test_delete_job():
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete(f"/jobs/{job_id}", headers=headers)
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get("/jobs/", headers=headers)
    assert len(response.json()) == 0