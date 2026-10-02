from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Job
from schemas import JobIn, JobOut

app = FastAPI()
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(engine)


@app.get("/")
def home():
    return {"message": "job board is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs", response_model=JobOut, status_code=201)
def create_job(data: JobIn, db: Session = Depends(get_db)):
    job = Job(**data.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@app.get("/jobs", response_model=list[JobOut])
def list_jobs(db: Session = Depends(get_db)):
    return db.scalars(select(Job)).all()

@app.get("/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.put("/jobs/{job_id}", response_model=JobOut)
def update_job(job_id: int, data: JobIn, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    job.title = data.title
    job.description = data.description
    job.status = data.status
    db.commit()
    db.refresh(job)
    return job


@app.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()


@app.get("/board", include_in_schema=False)
def board(request: Request, db: Session = Depends(get_db)):
    jobs = db.scalars(select(Job)).all()
    return templates.TemplateResponse(request, "board.html", {"jobs": jobs})

@app.post("/board/new", include_in_schema=False)
def board_create(
    title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    db.add(Job(title=title, description=description))
    db.commit()
    return RedirectResponse("/board", status_code=303)


@app.post("/board/{job_id}/delete", include_in_schema=False)
def board_delete(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if job is not None:
        db.delete(job)
        db.commit()
    return RedirectResponse("/board", status_code=303)


@app.get("/board/{job_id}/edit", include_in_schema=False)
def board_edit_form(job_id: int, request: Request, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return templates.TemplateResponse(request, "edit.html", {"job": job})


@app.post("/board/{job_id}/edit", include_in_schema=False)
def board_edit_save(
    job_id: int,
    title: str = Form(...),
    description: str = Form(""),
    status: str = Form("open"),
    db: Session = Depends(get_db),
):
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    job.title = title
    job.description = description
    job.status = status
    db.commit()
    return RedirectResponse("/board", status_code=303)