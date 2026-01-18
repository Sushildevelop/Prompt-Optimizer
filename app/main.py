from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.v1.endpoints.api import api_router
from app.utils.logger import app_logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


scheduler = AsyncIOScheduler()


async def scheduled_sync():
    print("Running scheduled sync task...")



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    app_logger.info("Starting up application...")
    await connect_to_mongo()
    app_logger.info("Database connection established")

    # Add a cron job
    scheduler.add_job(
       scheduled_sync,
        CronTrigger(minute="*/59"),  # Every 30 minute
        id="my_cron_job",
        replace_existing=True
    )
    scheduler.start()
    app_logger.info("Scheduler started with cron jobs")

    
    yield
    
    # Shutdown
    app_logger.info("Shutting down application...")
    await close_mongo_connection()
    app_logger.info("Database connection closed")


# Create FastAPI app
app = FastAPI(
    title=settings.project_name,
    description="""Welcome to the Prompt Optimizer API documentation.
        Prompt Optimizer is a platform for optimizing prompts and enhancing AI interactions.
        The API documentation provides detailed information about the endpoints""",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    app_logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": "1.0.0"
    }


# Include API routes
app.include_router(api_router, prefix=settings.api_v1_str)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to the Prompt Optimizer API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_check": "/health"
    }

@app.get("/debug/cron-jobs")
async def list_cron_jobs():
    """Return all registered APScheduler jobs"""
    jobs = scheduler.get_jobs()
    return [
        {
            "id": job.id,
            "func": str(job.func),
            "trigger": str(job.trigger),
            "next_run_time": str(job.next_run_time)
        }
        for job in jobs
    ]


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.environment == "development" else False,
        log_level=settings.log_level.lower()
    )
