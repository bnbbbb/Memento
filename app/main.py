from fastapi import FastAPI
from api import endpoints
from pydantic import BaseModel
from typing import Optional
from utils.scheduler import scheduler
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown()
        
app = FastAPI(lifespan=lifespan)

class URLRequest(BaseModel):
    url: str
    expires_at: Optional[str] = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진 허용 (혹은 특정 오리진만 허용할 수 있습니다)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

app.include_router(endpoints.router)
