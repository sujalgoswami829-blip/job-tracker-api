# Job Application Tracker API

A backend API built with FastAPI and PostgreSQL where users can register, log in, and track their job applications.

## Features
- User Registration & JWT Authentication
- CRUD operations for job applications (Create, Read, Update, Delete)
- Filter jobs by status (Applied, Interview, Offer, Rejected)
- Search jobs by company name
- Fully Dockerized
- CI/CD with GitHub Actions (10 passing tests)
- Deployed on Render

## Tech Stack
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (PyJWT) & Bcrypt
- **Testing:** Pytest
- **Deployment:** Render

## Live API
Check out the live Swagger documentation here: 
👉 **[https://job-tracker-api-qv0w.onrender.com/docs]** *(Paste your Render link followed by /docs here)*

## How to Run Locally (with Docker)
1. Clone the repo: `git clone <your-repo-link>`
2. Go to the folder: `cd job-tracker-api`
3. Run Docker: `docker compose up --build`
4. Open `http://127.0.0.1:8000/docs`

*(Note: You need Docker Desktop installed for this to work).*