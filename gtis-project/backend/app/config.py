import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_TITLE: str = "Global Trend Intelligence System"
    API_VERSION: str = "1.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DATABASE_URL: str = "sqlite:///data/gtis.db"
    MODEL_CACHE_DIR: str = "models/cache"
    PYTRENDS_RATE_LIMIT: int = 1
    DEFAULT_PREDICTION_PERIODS: int = 30
    FORECAST_CONFIDENCE_LEVEL: float = 0.95
    
    class Config:
        env_file = ".env"

settings = Settings()
