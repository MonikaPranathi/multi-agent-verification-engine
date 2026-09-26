from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from main import run_pipeline

app = FastAPI(
    title="Multi-Agent Verification Engine",
    description="AI-powered supply chain disruption verification system"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "message": "Multi-Agent Verification Engine API is running"
    }


@app.post("/verify")
def verify_disruption(data: dict):

    disruption = data.get("disruption", "")

    if not disruption:
        return {
            "error": "Disruption description is required"
        }

    result = run_pipeline(disruption)

    return result
