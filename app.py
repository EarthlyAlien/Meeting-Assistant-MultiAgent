import os
import json
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
from dotenv import load_dotenv
from orchestrator import MeetingAssistantOrchestrator

# Load environment variables
load_dotenv()

app = FastAPI(title="Meeting Assistant")

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

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/process")
async def process_meeting(
    file: UploadFile = File(...),
    openai_api_key: Optional[str] = Form(None),
    azure_speech_key: Optional[str] = Form(None)
):
    """Process a meeting recording"""
    try:
        # Save the uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Configure the orchestrator
        config = {
            "openai_api_key": openai_api_key or os.getenv("OPENAI_API_KEY"),
            "azure_speech_key": azure_speech_key or os.getenv("AZURE_SPEECH_KEY")
        }
        
        # Process the meeting
        orchestrator = MeetingAssistantOrchestrator(config)
        results = orchestrator.process_meeting(str(file_path))
        
        # Generate report
        report = orchestrator.generate_report(results)
        
        # Save results and report with unique names based on timestamp
        results_file = UPLOAD_DIR / f"results_{file.filename}.json"
        report_file = UPLOAD_DIR / f"report_{file.filename}.md"
        
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        
        with open(report_file, "w") as f:
            f.write(report)
        
        # Clean up the uploaded audio file
        os.remove(file_path)
        
        return JSONResponse({
            "status": "success",
            "message": "Meeting processed successfully",
            "results": results,
            "report": report
        })
        
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 