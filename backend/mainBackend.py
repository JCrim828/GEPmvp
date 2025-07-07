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

origins = [
    "http://localhost:3000"
    
    ]

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
    "jackC": ["JackCriminger"] #for testing purposes
}

# Request models
class LogEntry(BaseModel):
    url: str
    user_agent: str
    access_time: datetime
    frequency: int
    raw_text: str
    crawler: Optional[str] = None

class LogBatch(BaseModel):
    logs: List[LogEntry]

def detect_ai_crawler(user_agent: str) -> Optional[str]:
    for crawler, markers in AI_CRAWLERS.items():
        if any(marker in user_agent for marker in markers):
            return crawler
    return None

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
                frequency=log.frequency,
                raw_text=log.raw_text
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

@app.get("/test_claude")
async def test_claude():
    prompt = "what are the first 6 letters in the alphabet?"
    response = await call_claude(prompt)
    print(response)
    return {"claude_response": response.get("content", "No response")}

@app.get("/get_logs", response_model = LogBatch)
async def get_logs(db: Session = Depends(get_db)):
    logs = db.query(CrawlerLog).all()
    return {"logs": logs}

@app.get("/responses", response_model=List[str])
async def get_responses(db: Session=Depends(get_db)):
    responses = db.query(CrawlerLog.raw_text).all()
    return [r[0] for r in responses]

if __name__ == "__main__":
    uvicorn.run("mainBackend:app", host="0.0.0.0", port=8000, reload=True)