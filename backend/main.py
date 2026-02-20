from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

from backend.schemas import (
    ChildDetails, 
    AstrologyRequest, AstrologyOutput,
    InsightsRequest, InsightsOutput,
    TipsRequest, TipsOutput,
    TasksRequest, TasksOutput,
    FullReportResponse
)

from backend.services.astrology_service import generate_astrology_data
from backend.services.insights_service import generate_insights_data
from backend.services.parenting_service import generate_parenting_tips_data
from backend.services.tasks_service import generate_tasks_data

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for Logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Identify endpoint
    path = request.url.path
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Path: {path} | Method: {request.method} | Status: {response.status_code} | Duration: {process_time:.4f}s")
    
    return response

@app.get("/")
def read_root():
    return {"status": "running", "message": "Parenting Guide API is operational. Access docs at /docs"}

# --- v1 API Endpoints ---

@app.post("/api/v1/generate-astrology", response_model=AstrologyOutput)
def generate_astrology(request: AstrologyRequest):
    logger.info("Generating Astrology Data...")
    try:
        return generate_astrology_data(request.child_details)
    except Exception as e:
        logger.error(f"Error generating astrology: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/generate-insights", response_model=InsightsOutput)
def generate_insights(request: InsightsRequest):
    logger.info("Generating Insights Data...")
    try:
        return generate_insights_data(request.child_details, request.astrology_output)
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/generate-parenting-tips", response_model=TipsOutput)
def generate_parenting_tips(request: TipsRequest):
    logger.info("Generating Parenting Tips...")
    try:
        return generate_parenting_tips_data(request.child_details, request.insights_output)
    except Exception as e:
        logger.error(f"Error generating parenting tips: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/generate-daily-tasks", response_model=TasksOutput)
def generate_tasks(request: TasksRequest):
    logger.info("Generating Daily Tasks...")
    try:
        return generate_tasks_data(request.child_details, request.tips_output)
    except Exception as e:
        logger.error(f"Error generating tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/generate-full-report", response_model=FullReportResponse)
def generate_full_report(request: ChildDetails):
    logger.info("Generating Full Report (Orchestrator)...")
    try:
        # Sequential Generation Chain
        astrology = generate_astrology_data(request)
        insights = generate_insights_data(request, astrology)
        tips = generate_parenting_tips_data(request, insights)
        tasks = generate_tasks_data(request, tips)
        
        return FullReportResponse(
            astrology=astrology,
            insights=insights,
            parenting_tips=tips,
            daily_tasks=tasks
        )
    except Exception as e:
        logger.error(f"Error generating full report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
