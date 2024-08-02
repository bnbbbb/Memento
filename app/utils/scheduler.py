from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from database.connection import engine
from app.models.models import URL

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# scheduler 하루를 기준으로 현재 시간보다 전에 있는 db를 찾아서 지우게 만들었음. 

def delete_expired_url():
    db = SessionLocal()
    try:
        current_time = datetime.now()
        expired_urls = db.query(URL).filter(URL.expires_at < current_time).all()
        for url in expired_urls:
            print(url)
            db.delete(url)
        db.commit()
    finally:
        db.close()    

scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_url, 'interval', days=1)
    