import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, CrawlerLog
from claude_api import call_claude

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crawler detection
AI_CRAWLERS = {
    "Google-Extended": ["Google-Extended"],
    "GPTBot": ["GPTBot"],
    "PerplexityBot": ["PerplexityBot"],
}

def detect_ai_crawler(user_agent: str) -> Optional[str]:
    for crawler, markers in AI_CRAWLERS.items():
        if any(marker in user_agent for marker in markers):
            return crawler
    return None

# Request models
class LogEntry(BaseModel):
    url: str
    user_agent: str
    access_time: datetime
    frequency: int

class LogBatch(BaseModel):
    logs: List[LogEntry]

@app.post("/logs/ingest")
async def ingest_logs(log_batch: LogBatch, db: Session = Depends(get_db)):
    saved = []
    for log in log_batch.logs:
        crawler = detect_ai_crawler(log.user_agent)
        if crawler:
            db_log = CrawlerLog(
                url=log.url,
                user_agent=log.user_agent,
                crawler=crawler,
                access_time=log.access_time,
                frequency=log.frequency
            )
            db.add(db_log)
            saved.append(db_log)
    db.commit()

    if not saved:
        raise HTTPException(status_code=400, detail="No AI crawler logs found.")

    # Optional: Call Claude with summary
    summary_prompt = f"{len(saved)} logs ingested. First URL: {saved[0].url}"
    claude_response = await call_claude(summary_prompt)

    return {
        "saved_logs": len(saved),
        "claude_summary": claude_response.get("content", "No response from Claude.")
    }

if __name__ == "__main__":
    uvicorn.run("mainBackend:app", host="0.0.0.0", port=8000, reload=True)