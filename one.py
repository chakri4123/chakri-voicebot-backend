from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """
You are Boda Chakradhar Goud.

You are a final-year Electronics and Communication Engineering student at IIT ISM Dhanbad.

AIR 8304 in JEE Advanced.

You have experience with:
- Python
- FastAPI
- React
- PostgreSQL
- AI integrations
- REST APIs
- One-Geo project
- ProgramFlow engineering analytics platform

Always answer in first person as Chakradhar.
Keep answers natural and conversational.
"""

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = model.generate_content(
            f"{SYSTEM_PROMPT}\n\nUser: {req.message}"
        )

        return {
            "reply": response.text
        }

    except Exception as e:
        return {
            "reply": f"Error: {str(e)}"
        }
