"""Application Configuration"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Backend
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    debug: bool = True
    
    # Frontend
    frontend_port: int = 8501
    
    # Database
    database_url: str = "sqlite:///threat_intelligence.db"
    
    # ML
    model_path: str = "ml/models/isolation_forest_model.pkl"
    anomaly_threshold: float = 0.7
    
    # Security
    secret_key: str = "your-secret-key-here"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        protected_namespaces = ('settings_',)


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance"""
    return Settings()
