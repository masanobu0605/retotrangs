from __future__ import annotations

from functools import lru_cache
from pydantic import BaseModel, Field
import os
from typing import Optional
import sys


class Settings(BaseModel):
    app_name: str = "python-api"
    session_secret: str = Field(default=os.getenv("SESSION_SECRET", "devsupersecret"))
    # Prefer DB_URL (PostgreSQL) over SQLite path. Example: postgresql+psycopg2://user:pass@db:5432/app
    db_url: Optional[str] = Field(default=os.getenv("DB_URL"))
    db_path: str = Field(default=os.getenv(
        "DB_PATH",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.db")),
    ))
    cors_origins: str = Field(default=os.getenv("CORS_ORIGINS", "http://localhost:3000"))
    admin_email: str = Field(default=os.getenv("ADMIN_EMAIL", "admin@example.com"))
    admin_password: str = Field(default=os.getenv("ADMIN_PASSWORD", "admin123"))
    # Testing flag: enabled when TESTING=1 or running under pytest
    testing: bool = Field(
        default=(os.getenv("TESTING", "0") == "1" or "PYTEST_CURRENT_TEST" in os.environ)
    )

    def effective_db_url(self) -> str:
        if self.db_url:
            return self.db_url
        if self.testing or "pytest" in sys.modules or os.getenv("PYTEST_CURRENT_TEST"):
            test_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "app.test.db")
            )
            return f"sqlite:///{test_path}"
        return f"sqlite:///{self.db_path}"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
