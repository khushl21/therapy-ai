from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data["prompt"]

    

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "therapy",
        "prompt": prompt,
        "stream": False
    })

    return {"reply": response.json()["response"]}
