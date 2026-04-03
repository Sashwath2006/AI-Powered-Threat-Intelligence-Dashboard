"""FastAPI Application Factory"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pathlib import Path
import os

from app.config import get_settings
from app.api.routes import router as api_router, set_detector
from app.ml.anomaly_detector import AnomalyDetector
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    
    Returns:
        FastAPI application instance
    """
    app = FastAPI(
        title="Threat Intelligence API",
        description="AI-Powered threat detection using Isolation Forest",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"{request.method} {request.url.path} - Status: {response.status_code}")
        return response
    
    # Include API routes
    app.include_router(api_router, prefix="/api", tags=["API"])
    
    # Health check endpoint
    @app.get(
        "/health",
        summary="Health check",
        tags=["System"]
    )
    async def health_check():
        """Simple health check"""
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "Threat Intelligence API"
        }
    
    # Root endpoint
    @app.get("/", tags=["System"])
    async def root():
        """API root endpoint"""
        return {
            "service": "Threat Intelligence API",
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    
    # Startup event
    @app.on_event("startup")
    async def startup_event():
        """Initialize ML model on startup"""
        logger.info("Starting up Threat Intelligence API...")
        
        try:
            # Initialize anomaly detector
            detector = AnomalyDetector(contamination=0.1)
            
            # Try to load pre-trained model
            model_path = settings.model_path
            if os.path.exists(model_path):
                try:
                    detector.load_model(model_path)
                    logger.info(f"Loaded pre-trained model from {model_path}")
                except Exception as e:
                    logger.warning(f"Could not load pre-trained model: {e}")
                    logger.info("Using fresh model for training")
                    # Create sample training data and train
                    _train_sample_model(detector)
            else:
                logger.info("No pre-trained model found, creating fresh model")
                _train_sample_model(detector)
            
            # Set detector in routes
            set_detector(detector)
            logger.info("API startup complete")
            
        except Exception as e:
            logger.error(f"Error during startup: {e}")
            raise
    
    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown"""
        logger.info("Shutting down Threat Intelligence API...")
    
    return app


def _train_sample_model(detector: AnomalyDetector) -> None:
    """
    Train model with sample data
    
    Args:
        detector: AnomalyDetector instance
    """
    import numpy as np
    
    # Generate sample training data
    # Normal network traffic patterns
    normal_samples = np.random.normal(
        loc=[443, 1024, 2048, 5.0],  # port, bytes_sent, bytes_received, duration
        scale=[100, 512, 512, 2.0],
        size=(900, 4)
    )
    
    # Anomalous patterns (different statistics)
    anomalous_samples = np.random.normal(
        loc=[8000, 10240, 51200, 30.0],
        scale=[1000, 5120, 10240, 10.0],
        size=(100, 4)
    )
    
    # Combine and train
    training_data = np.vstack([normal_samples, anomalous_samples])
    detector.train(training_data)
    
    # Save model
    Path(settings.model_path).parent.mkdir(parents=True, exist_ok=True)
    detector.save_model(settings.model_path)
    logger.info(f"Trained and saved fresh model to {settings.model_path}")


# Create application instance
app = create_app()
