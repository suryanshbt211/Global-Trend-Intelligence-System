from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
import pandas as pd

from app.services.pytrends_service import PyTrendsService
from app.models.trend_predictor import TrendPredictor
from app.models.nlp_analyzer import NLPAnalyzer
from app.services.correlation_service import CorrelationService
from app.database.db_manager import DatabaseManager

app = FastAPI(
    title="Global Trend Intelligence System API",
    description="AI-driven analytics platform for predicting global search trends",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pytrends_service = PyTrendsService()
trend_predictor = TrendPredictor()
nlp_analyzer = NLPAnalyzer()
correlation_service = CorrelationService()
db_manager = DatabaseManager()

class TrendRequest(BaseModel):
    keywords: List[str]
    timeframe: str = "today 12-m"
    geo: str = ""

class PredictionRequest(BaseModel):
    keyword: str
    periods: int = 30

class CorrelationRequest(BaseModel):
    keyword: str
    external_data_source: str

@app.get("/")
async def root():
    return {
        "message": "Global Trend Intelligence System API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.post("/api/fetch-trends")
async def fetch_trends(request: TrendRequest):
    try:
        data = pytrends_service.fetch_interest_over_time(
            keywords=request.keywords,
            timeframe=request.timeframe,
            geo=request.geo
        )
        db_manager.store_trends(data, request.keywords)
        return {
            "status": "success",
            "data": data.to_dict(orient="records"),
            "keywords": request.keywords
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict-trends")
async def predict_trends(request: PredictionRequest):
    try:
        historical_data = db_manager.get_trend_history(request.keyword)
        if historical_data.empty:
            historical_data = pytrends_service.fetch_interest_over_time(
                keywords=[request.keyword],
                timeframe="today 12-m"
            )
        predictions = trend_predictor.predict(
            data=historical_data,
            keyword=request.keyword,
            periods=request.periods
        )
        return {
            "status": "success",
            "keyword": request.keyword,
            "predictions": predictions,
            "model_performance": trend_predictor.get_model_metrics()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/related-queries/{keyword}")
async def get_related_queries(keyword: str):
    try:
        related = pytrends_service.get_related_queries(keyword)
        topics = nlp_analyzer.cluster_related_topics(related)
        return {
            "status": "success",
            "keyword": keyword,
            "related_queries": related,
            "topic_clusters": topics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/regional-interest/{keyword}")
async def get_regional_interest(keyword: str):
    try:
        regional_data = pytrends_service.get_interest_by_region(keyword)
        return {
            "status": "success",
            "keyword": keyword,
            "regional_data": regional_data.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/correlations")
async def analyze_correlations(request: CorrelationRequest):
    try:
        correlations = correlation_service.compute_correlations(
            keyword=request.keyword,
            external_source=request.external_data_source
        )
        return {
            "status": "success",
            "keyword": request.keyword,
            "correlations": correlations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/emerging-topics")
async def detect_emerging_topics():
    try:
        emerging = pytrends_service.detect_emerging_trends()
        return {
            "status": "success",
            "emerging_topics": emerging,
            "detection_time": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": db_manager.check_connection(),
            "pytrends": True,
            "ml_models": trend_predictor.is_ready()
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
