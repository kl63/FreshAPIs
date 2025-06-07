import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/freshly_supermarket"
    )
    
    # Application settings
    APP_NAME: str = "Freshly Supermarket API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Your go-to grocery backend!"
    
    # Testing
    TESTING: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a global settings instance
settings = Settings()
