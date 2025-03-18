import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from orchestrator import MeetingAssistantOrchestrator

from meeting_assistant.config import load_config

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Meeting Assistant API",
    description="API for processing meeting recordings using multi-agent system",
    version="1.0.0",
)

# Create directories for static files and templates
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
UPLOAD_DIR = BASE_DIR / "uploads"

# Create directories if they don't exist
STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Initialize the orchestrator
config = load_config()
orchestrator = MeetingAssistantOrchestrator(config)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process-meeting")
async def process_meeting(audio_file: UploadFile = File(...)) -> Dict[str, Any]:
    """Process a meeting recording.

    Args:
        audio_file: The uploaded meeting audio file.

    Returns:
        Dict containing the processing results.

    Raises:
        HTTPException: If file upload or processing fails.
    """
    try:
        # Save uploaded file
        temp_path = f"temp/{audio_file.filename}"
        with open(temp_path, "wb") as f:
            content = await audio_file.read()
            f.write(content)

        # Process the meeting
        results = orchestrator.process_meeting(temp_path)

        # Clean up
        os.remove(temp_path)

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process meeting: {str(e)}"
        )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Check the health of the API.

    Returns:
        Dict containing status information.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    # Use environment variable for host in production, default to localhost
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))

    # Enable reload only in development
    reload = os.getenv("API_ENV", "development").lower() == "development"

    uvicorn.run("app:app", host=host, port=port, reload=reload)
