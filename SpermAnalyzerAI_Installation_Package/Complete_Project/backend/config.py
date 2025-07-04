"""
Configuration settings for Sperm Analyzer AI Backend
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sperm Analyzer AI"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "sperm-analyzer-ai-secret-key-2025"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DATABASE_URL: str = "sqlite:///./sperm_analyzer.db"
    
    # AI Models
    YOLO_MODEL_PATH: str = "models/yolov8n.pt"
    DETECTION_CONFIDENCE: float = 0.5
    TRACKING_MAX_AGE: int = 30
    
    # File upload
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    UPLOAD_DIR: str = "uploads"
    
    # CASA parameters
    FRAME_RATE: int = 30
    MICRONS_PER_PIXEL: float = 0.5
    CHAMBER_DEPTH: float = 20.0  # micrometers
    
    class Config:
        env_file = ".env"

settings = Settings()
