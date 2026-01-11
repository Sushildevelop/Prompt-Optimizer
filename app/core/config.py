from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "prompt_optimizer_db"
    
    # Security
    secret_key: str = "sushi_is_awesome"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Environment
    environment: str = "development"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"

    
    openai_api_key: str
    atlas_connection_string: str



    # Logging
    log_level: str = "INFO"
    log_file_path: str = "./logs/app.log"
    
    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "Prompt Optimizer"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()

# Ensure logs directory exists
os.makedirs(os.path.dirname(settings.log_file_path), exist_ok=True)