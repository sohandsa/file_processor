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
    job.progress = 0
    db.commit()

    try:
        for i in range(1, 11):
            time.sleep(0.5)  # simulate work step
            job.progress = i * 10  # 10%, 20%, ..., 100%
            db.commit()

        job.status = "done"
        db.commit()
    except Exception:
        job.status = "failed"
        job.progress = 0
        db.commit()
    finally:
        db.close()

