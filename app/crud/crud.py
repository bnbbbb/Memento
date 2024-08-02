from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from app.models.models import URL
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
import secrets
import string

def generate_short_key(db: Session, length: int = 6, max_attempts: int = 10) -> str:
    # Base62 
    characters = string.ascii_letters + string.digits
    # 효율성을 위해 10번 정도 실행하게 하였습니다.
    for _ in range(max_attempts):
        short_key = ''.join(secrets.choice(characters) for _ in range(length))
        existing_url = db.query(URL).filter_by(short_key=short_key).first()
        if not existing_url:
            return short_key
    raise ValueError("short key를 생성하는데 실패하였습니다.")

def create_url(db: Session, url: schemas.URLCreate) -> schemas.URLResponse:
    try:
        short_key = generate_short_key(db)
        # 만료시간이 선택하게 되면 그 값을 일로 계산하였고, 선택되지 않으면 기본값 10으로 설정하였습니다.
        expires_at = url.expires_at or (datetime.now() + timedelta(days=10))
        db_url = URL(short_key=short_key, original_url=url.url, expires_at=expires_at)
        db.add(db_url)
        db.commit()
        return schemas.URLResponse(short_url=f"http://localhost:8000/{short_key}")
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def get_url(db: Session, short_key: str):
    url = db.query(models.URL).filter(models.URL.short_key == short_key).first()
    if url is None:
        raise HTTPException(status_code=404, detail="short_key가 존재 하지 않습니다.")
    return url

def increment_visit_count(db: Session, url_id: int):
    stats = db.query(models.Statistics).filter(models.Statistics.url_id == url_id).first()
    if stats:
        stats.visit_count += 1
        stats.last_visited = datetime.now()
    else:
        stats = models.Statistics(url_id=url_id, visit_count=1, last_visited=datetime.now())
        db.add(stats)
    db.commit()
    
def is_valid_url(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")