from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.crud import crud
from app.models import models
from app.schemas import schemas
from database import connection

router = APIRouter()

@router.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(url: schemas.URLCreate, db: Session = Depends(connection.get_db)):
    if not crud.is_valid_url(url.url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    db_url = crud.create_url(db, url)
    return db_url

@router.get("/{short_key}")
def redirect_to_url(short_key: str, db: Session = Depends(connection.get_db)):
    db_url = crud.get_url(db, short_key)
    crud.increment_visit_count(db, db_url.id)
    return RedirectResponse(db_url.original_url, status_code=301)

@router.get("/stats/{short_key}", response_model=schemas.StatisticsResponse)
def get_statistics(short_key: str, db: Session = Depends(connection.get_db)):
    db_url = crud.get_url(db, short_key)
    if db_url:
        stats = db.query(models.Statistics).filter(models.Statistics.url_id == db_url.id).first()
        if stats:
            return schemas.StatisticsResponse(visit_count=stats.visit_count, last_visited=stats.last_visited)
        return schemas.StatisticsResponse(visit_count=0, last_visited=None)
    raise HTTPException(status_code=404, detail="URL not found")