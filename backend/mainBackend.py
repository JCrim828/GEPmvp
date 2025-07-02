import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
claude_api_key = os.getenv("CLAUDE_API_KEY") # claude api key

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


class LogEntry(BaseModel):
    url: str 
    user: str 
    access_time: datetime
    frequency: int

class LogBatch(BaseModel):
    logs: List[LogEntry]

# AI crawler detection logic
AI_CRAWLERS = {
    "Google-Extended": ["Google-Extended"],
    "GPTBot": ["GPTBot"],
    "PerplexityBot": ["PerplexityBot"],
}

def detect_ai_crawler(user_agent: str) -> Optional[str]:
    for crawler_name, identifiers in AI_CRAWLERS.items():
        if any(idf in user_agent for idf in identifiers):
            return crawler_name
    return None

#Routes
@app.get("/")
def read_root():
    return "test read route"

@app.post("/logs/ingest")
def ingest_logs(log_batch: LogBatch):
    processed = []
    for log in log_batch.logs:
        crawler = detect_ai_crawler(log.user_agent)
        if crawler:

            # Here you would insert into DB or update counts
            processed.append({
                "url": log.url,
                "crawler": crawler,
                "access_time": log.access_time.isoformat(),
                "frequency": log.frequency
            })
    if not processed:
        raise HTTPException(status_code=400, detail="No AI crawler logs found.")
    return {"processed_logs": processed, "count": len(processed)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

