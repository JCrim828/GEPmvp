from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class CrawlerLog(Base):
    __tablename__ = "crawler_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(191), index=True)
    user_agent = Column(String(2048))
    crawler = Column(String(2048))
    access_time = Column(DateTime)
    frequency = Column(Integer)