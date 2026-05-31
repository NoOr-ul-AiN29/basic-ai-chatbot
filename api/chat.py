from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from groq import Groq
from dotenv import load_dotenv
from utils.error_handler import handle_error

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful, friendly, and knowledgeable AI assistant.
You provide clear, concise, and accurate answers.
When you don't know something, you say so honestly."""

# Serve static files (index.html) from the public folder
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/")
async def root():
    return FileResponse("public/index.html")

@app.post("/api/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        conversation_history = body.get("messages", [])

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return JSONResponse({"reply": response.choices[0].message.content})

    except Exception as e:
        return JSONResponse({"reply": handle_error(e)}, status_code=200)
