from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.post("/", response_model=schemas.JobOut, status_code=status.HTTP_201_CREATED)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_job = models.Job(**job.model_dump(), user_id=current_user.id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/", response_model=List[schemas.JobOut])
def get_jobs(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    jobs = db.query(models.Job).filter(models.Job.user_id == current_user.id).all()
    return jobs

@router.put("/{job_id}", response_model=schemas.JobOut)
def update_job(job_id: int, job_update: schemas.JobUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    job_query = db.query(models.Job).filter(models.Job.id == job_id, models.Job.user_id == current_user.id)
    job = job_query.first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    update_data = job_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)
    return job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    job_query = db.query(models.Job).filter(models.Job.id == job_id, models.Job.user_id == current_user.id)
    job = job_query.first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    job_query.delete(synchronize_session=False)
    db.commit()
    return None