import os
from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./dev.db"
    SECRET_KEY: str = "dev-secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    AZURE_CLIENT_ID: str | None = None
    AZURE_CLIENT_SECRET: str | None = None
    AZURE_TENANT_ID: str | None = None
    MSAL_REDIRECT_URI: str = "http://localhost:8000/api/outlook/callback"

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        env_file_encoding = "utf-8"

settings = Settings()