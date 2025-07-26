from celery import Celery
from app.db.connection import SessionLocal
from app.models.job import Job
import time

celery = Celery("tasks", broker="memory://localhost/")

@celery.task
def process_file(job_id: str):
    db = SessionLocal()
    job = db.query(Job).filter_by(id=job_id).first()
    job.status = "processing"
    db.commit()

    try:
        time.sleep(5)
        job.status = "done"
    except:
        job.status = "failed"
    
    db.commit()
    db.close()
