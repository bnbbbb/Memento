from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

class URL(Base):
    __tablename__ = 'urls'
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False, index=True)
    short_key = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    expires_at = Column(DateTime, default=None, nullable=True)

    stats = relationship("Statistics", uselist=False, back_populates="url")

class Statistics(Base):
    __tablename__ = 'statistics'
    
    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey('urls.id'), unique=True)
    visit_count = Column(Integer, default=0)
    last_visited = Column(DateTime, nullable=True)

    url = relationship("URL", back_populates="stats")