"""
Sperm Analyzer AI - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from pathlib import Path
import asyncio
from datetime import datetime
import uuid

from backend.config import settings
from backend.routes import analysis, health
from backend.services.video_processor import VideoProcessor
from backend.services.sperm_detector import SpermDetector
from backend.services.sperm_tracker import SpermTracker
from backend.services.casa_calculator import CASACalculator

# Create FastAPI app
app = FastAPI(
    title="Sperm Analyzer AI API",
    description="AI-powered sperm analysis system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")

# Initialize services
video_processor = VideoProcessor()
sperm_detector = SpermDetector()
sperm_tracker = SpermTracker()
casa_calculator = CASACalculator()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sperm Analyzer AI API",
        "version": "1.0.0",
        "status": "operational",
        "developer": "Youssef Shtaiwi",
        "docs": "/docs"
    }

@app.post("/analyze")
async def analyze_sample(file: UploadFile = File(...)):
    """Main analysis endpoint"""
    try:
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / f"{job_id}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process video/image
        frames = await video_processor.extract_frames(file_path)
        
        # Detect sperm
        detections = []
        for frame in frames:
            detection = await sperm_detector.detect(frame)
            detections.append(detection)
        
        # Track sperm movement
        tracks = await sperm_tracker.track(detections)
        
        # Calculate CASA metrics
        casa_metrics = await casa_calculator.calculate(tracks)
        
        # Prepare results
        results = {
            "job_id": job_id,
            "timestamp": datetime.now().isoformat(),
            "filename": file.filename,
            "analysis": {
                "sperm_count": casa_metrics["count"],
                "concentration": casa_metrics["concentration"],
                "motility": {
                    "progressive": casa_metrics["progressive_motility"],
                    "non_progressive": casa_metrics["non_progressive_motility"],
                    "immotile": casa_metrics["immotile"]
                },
                "velocities": {
                    "vcl": casa_metrics["vcl"],
                    "vsl": casa_metrics["vsl"],
                    "vap": casa_metrics["vap"]
                },
                "linearity": casa_metrics["linearity"],
                "morphology": {
                    "normal": casa_metrics["normal_morphology"],
                    "abnormal": casa_metrics["abnormal_morphology"]
                }
            },
            "processing_time": casa_metrics["processing_time"],
            "status": "completed"
        }
        
        return JSONResponse(content=results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
