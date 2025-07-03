import httpx
import os
from dotenv import load_dotenv

load_dotenv()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

async def call_claude(prompt: str):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "content-type": "application/json"
    }
    body = {
        "model": "claude-3-opus-20240229",  # or any available Claude model
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 256,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.anthropic.com/v1/messages", json=body, headers=headers)
        return response.json()