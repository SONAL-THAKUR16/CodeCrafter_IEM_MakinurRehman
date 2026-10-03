import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routes.analysis import router as analysis_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("student_analyzer_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler to initialize SQLite database and load/cache Hugging Face NLP models once during app startup."""
    logger.info("[STARTUP] Initializing SQLite database tables...")
    try:
        from app.database import init_db
        init_db()
        logger.info("[STARTUP] Database tables initialized successfully.")
    except Exception as db_exc:
        logger.error(f"[STARTUP] Error initializing database tables: {db_exc}")

    logger.info("[STARTUP] Initializing NLP model pipelines...")
    try:
        from app.services.sentiment_service import _load_sentiment_model
        from app.services.emotion_service import _load_emotion_model
        _load_sentiment_model()
        _load_emotion_model()
        logger.info("[STARTUP] NLP model initialization complete. Ready for requests.")
    except Exception as exc:
        logger.warning(f"[STARTUP] NLP model warmup deferred or encountered exception: {exc}")
    yield


app = FastAPI(
    title="Student Academic Experience & Emotion Analysis API",
    description=(
        "AI-powered context-aware backend system to analyze student academic feedback "
        "for indications of stress, cognitive overload, frustration, disengagement, and workload difficulty."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Configuration
raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173")
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include analysis routes
app.include_router(analysis_router)


@app.get("/", include_in_schema=False)
def root():
    return {
        "status": "online",
        "service": "student-emotional-analysis-api",
        "documentation": "/docs",
        "version": "2.0.0"
    }


@app.get("/api/health", summary="API Health Check", tags=["Health"])
def health_check():
    """Health check endpoint to verify backend service status."""
    return {
        "status": "ok",
        "service": "student-emotional-analysis-api"
    }


# Custom Exception Handlers for Clean Error Responses
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Clean JSON response for request validation errors."""
    errors = []
    for err in exc.errors():
        field = " -> ".join([str(loc) for loc in err.get("loc", []) if loc != "body"])
        msg = err.get("msg", "Invalid value")
        errors.append(f"{field}: {msg}" if field else msg)

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation Error",
            "details": errors
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to catch unhandled exceptions cleanly."""
    logger.error(f"Unhandled server error on {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please check backend logs."
        }
    )
