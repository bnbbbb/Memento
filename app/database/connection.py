from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from pathlib import Path

# .env 파일을 app폴더에 저장할 때
# BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
# .env 파일을 외부에 저장할 때
BASE_DIR = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=BASE_DIR)

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    print(BASE_DIR)
    try:
        yield db
    finally:
        db.close()
        
