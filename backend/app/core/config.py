import sys
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, HttpUrl, validator
from pydantic.networks import AnyHttpUrl

load_dotenv("../.env")


class Settings(BaseSettings):
    PROJECT_NAME: str = "fastapi-mongo-starter"

    SENTRY_DSN: Optional[HttpUrl] = None

    FRONTEND_URL: str = "http://localhost:3000"
    API_PATH: str = "/api/v1"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # need to set test values first, so initialization of validator can use it to override regular ones
    TEST_MONGODB_URL: str = "mongodb://mongodb:27017/test_database"
    TEST_MONGODB_DB_NAME: str = "test_database"
    MONGODB_URL: str = "mongodb://mongodb:27017/app_database"
    MONGODB_DB_NAME: str = "app_database"

    GOOGLE_OAUTH_CLIENT_ID: str = ""
    GOOGLE_OAUTH_CLIENT_SECRET: str = ""

    @validator("MONGODB_URL", pre=True)
    def override_mongodb_url_for_tests(cls, v: str, values: Dict[str, Any]):
        """Overrides MONGODB_URL with TEST_MONGODB_URL in test environment."""
        if "pytest" in sys.modules:
            test_url = values.get("TEST_MONGODB_URL")
            if test_url:
                return test_url
            else:
                raise Exception("pytest detected, but TEST_MONGODB_URL is not set in environment")
        return v

    @validator("MONGODB_DB_NAME", pre=True)
    def override_mongodb_db_name_for_tests(cls, v: str, values: Dict[str, Any]):
        """Overrides MONGODB_DB_NAME with TEST_MONGODB_DB_NAME in test environment."""
        if "pytest" in sys.modules:
            test_db_name = values.get("TEST_MONGODB_DB_NAME")
            if test_db_name:
                return test_db_name
            else:
                raise Exception("pytest detected, but TEST_MONGODB_DB_NAME is not set in environment")
        return v

    SECRET_KEY: str = ""
    #  END: required environment variables


settings = Settings()
