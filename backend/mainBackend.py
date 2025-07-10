import uvicorn
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, CrawlerLog
from claude_api import call_claude
import crawleruseragents
import requests
import gzip
import json
import io
import time
import boto3
from botocore import UNSIGNED
from botocore.config import Config

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

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#crawler dictionary
AI_CRAWLERS = {}
for entry in crawleruseragents.CRAWLER_USER_AGENTS_DATA:
    name = entry['pattern'].rstrip('\\/')
    user_agent = entry['instances'][0] if entry['instances'] else ''
    url = entry.get('url', '')

    AI_CRAWLERS[name] = {
        'user_agent': user_agent,
        'url': url
    }

#print(AI_CRAWLERS['GPTBot'])


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

def detect_ai_crawler(user_agent: str) -> Optional[Tuple[str, str]]:
    for pattern, info in AI_CRAWLERS.items():
        if pattern in user_agent:
            return pattern, info.get('url', '')
    return None

@app.get("/crawlers")
def get_all_crawlers():
    return AI_CRAWLERS

@app.post("/logs/ingest")
async def ingest_logs(log_batch: LogBatch, db: Session = Depends(get_db)):
    saved = []
    for log in log_batch.logs:
        crawler, crawler_url = detect_ai_crawler(log.user_agent)
        if crawler:
            db_log = CrawlerLog(
                url=crawler_url, #crawler url
                user_agent=log.user_agent,
                crawler=crawler,  #crawler name
                access_time=log.access_time,
                frequency=log.frequency,
                raw_text=log.raw_text
            )
            db.add(db_log)
            saved.append(db_log)
    db.commit()

    if not saved:
        raise HTTPException(status_code=400, detail="No AI crawler logs found.")

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

@app.post("/fetch_commoncrawl")
async def fetch_common_crawl(url: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_common_crawl, url)
    return {"message": f"Started background task for {url}"}

def sort_commoncrawl_collections(collections):
    def extract_sort_key(item):
        name = item.get("id", "")
        parts = name.split("-")
        if len(parts) != 3:
            return (0, 0)
        try:
            year = int(parts[2][:4])
            batch = int(parts[2][4:])
            return (year, batch)
        except:
            return (0, 0)
    return sorted(collections, key=extract_sort_key, reverse=True)

def process_common_crawl(url: str):
    db = SessionLocal()
    try:
        #get all collections and sort by most recent
        index_list_url = "https://index.commoncrawl.org/collinfo.json"
        res = requests.get(index_list_url)
        if res.status_code != 200:
            print("Failed to fetch index list")
            return

        all_indexes = res.json()
        sorted_indexes = sort_commoncrawl_collections(all_indexes)

        for index in sorted_indexes[:8]:
            query_url = f"{index['cdx-api']}?url={url}&output=json"
            print(f"Querying: {query_url}")
            entries = requests.get(query_url)
            if entries.status_code != 200:
                continue

            any_found = False
            for line in entries.iter_lines():
                data = json.loads(line)
                user_agent = data.get('user_agent', '')
                result = detect_ai_crawler(user_agent)
                if result:
                    crawler, crawler_url = result
                    warc_url = data['filename']
                    offset = data['offset']
                    length = data['length']
                    warc_prefix = "https://data.commoncrawl.org/"
                    full_url = f"{warc_prefix}{warc_url}"

                    headers = {"Range": f"bytes={offset}-{int(offset)+int(length)}"}
                    warc_res = requests.get(full_url, headers=headers)
                    if warc_res.status_code == 206:
                        try:
                            raw = gzip.decompress(warc_res.content).decode('utf-8', errors='ignore')
                            db_log = CrawlerLog(
                                submitted_url=url,
                                url=crawler_url,
                                user_agent=user_agent,
                                crawler=crawler,
                                access_time=datetime.utcnow(),
                                frequency=1,
                                raw_text=raw[:10000]
                            )
                            db.add(db_log)
                            any_found = True
                        except Exception as e:
                            print(f"Error decompressing/parsing WARC data: {e}")
            if any_found:
                db.commit()
                print("Successfully ingested crawl data")
                return  # Exit early once data is found

        print("No crawl entries found in recent indexes")

    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run("mainBackend:app", host="0.0.0.0", port=8000, reload=True)