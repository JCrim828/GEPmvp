from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from database import Base, SessionLocal

class CrawlerLog(Base):
    __tablename__ = "crawler_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(191), index=True)
    user_agent = Column(String(2048))
    crawler = Column(String(2048))
    access_time = Column(DateTime)
    frequency = Column(Integer)
    raw_text = Column(String(2048))