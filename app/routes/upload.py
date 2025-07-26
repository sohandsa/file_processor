from fastapi import APIRouter, File, UploadFile, WebSocket
from app.db.connection import SessionLocal
import asyncio
from app.internal.tasks import process_file
from app.models.job import Job
import uuid
import shutil

router = APIRouter(
    prefix="/rf",
    tags=["Robot Framework"],
)

@router.post("/")
async def output_loader(xmlFile: UploadFile = File(...)):
    job_id = str(uuid.uuid4)
    path = f"/tmp/{job_id}_{xmlFile.filename}"

    with open(path, "wb") as f:
        shutil.copyfileobj(xmlFile.file, f)
    
    db = SessionLocal()
    db.add(Job(id=job_id, status="queued"))
    db.commit()
    db.close()

    process_file.delay(job_id)
    if xmlFile.content_type != "text/xml":
        return {"error": f"only xml content is accepted {xmlFile.content_type}"}
    return {"content_type": xmlFile.content_type}


@router.websocket("/ws/{job_id}")
async def websocket_status(websocket: WebSocket, job_id: str):
    await websocket.accept()
    db = SessionLocal()

    try:
        while True:
            job = db.query(Job).filter_by(id=job_id).first()
            if job:
                await websocket.send_json({
                    "status": job.status,
                    "progress": job.progress
                })
                if job.status in ("done", "failed"):
                    break
            await asyncio.sleep(1)
    finally:
        db.close()
        await websocket.close()
