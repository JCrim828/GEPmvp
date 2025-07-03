from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class CrawlerLog(Base):
    __tablename__ = "crawler_logs"
    
    id_num = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    user_agent = Column(String)
    crawler = Column(String)
    access_time = Column(DateTime)
    frequency = Column(Integer)