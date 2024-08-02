from pydantic import BaseModel, validator, field_validator
from typing import Optional
from datetime import datetime, timedelta

class URLCreate(BaseModel):
    url: str
    expires_at: Optional[datetime] = None
    
    @field_validator('expires_at', mode='before')
    def parse_expires_at(cls, value):
        if value:
            # string, integer 상관없이 숫자이면 진행.
            if value.isdigit():
                # 현재 시간에 일로 추가
                return datetime.now() + timedelta(days=int(value))
            else:
                # 다른 문자가 들어오게되면 ValueError
                raise ValueError("유효하지 않은 데이터 포맷입니다.")
        return value

class URLResponse(BaseModel):
    short_url: str

class StatisticsResponse(BaseModel):
    visit_count: int
    last_visited: Optional[datetime] = None