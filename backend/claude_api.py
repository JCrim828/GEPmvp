import httpx
import os
from dotenv import load_dotenv

load_dotenv()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

HEADERS = {
    "x-api-key": CLAUDE_API_KEY,
    "anthropic-version": "2023-06-01",
    "Content-Type": "application/json"
}

async def call_claude(prompt: str) -> dict:
    payload = {
        "model": "claude-3-opus-20240229",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(CLAUDE_API_URL, headers=HEADERS, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print("Claude API error:", e)
            return {"content": "Claude call failed."}