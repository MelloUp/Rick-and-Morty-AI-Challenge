"""Application configuration management."""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass(frozen=True)
class DatabaseConfig:
    """Database configuration."""

    path: str = "rick_and_morty.db"
    test_path: str = "test_rick_and_morty.db"

    @property
    def connection_string(self) -> str:
        """Get database connection string."""
        return self.path


@dataclass(frozen=True)
class APIConfig:
    """External API configuration."""

    rick_morty_base_url: str = "https://rickandmortyapi.com/api"
    cache_ttl_minutes: int = 60
    request_timeout: int = 10
    max_retries: int = 3


@dataclass(frozen=True)
class GeminiConfig:
    """Gemini AI configuration."""

    api_key: Optional[str] = None
    model_name: str = "models/gemini-pro-latest"
    embedding_model: str = "models/text-embedding-004"
    max_tokens: int = 2048
    temperature: float = 0.7

    def __post_init__(self):
        """Load API key from environment."""
        if self.api_key is None:
            object.__setattr__(self, 'api_key', os.getenv('GEMINI_API_KEY'))

    @property
    def is_available(self) -> bool:
        """Check if Gemini is configured."""
        return self.api_key is not None and self.api_key != ""


@dataclass(frozen=True)
class FlaskConfig:
    """Flask application configuration."""

    debug: bool = True
    testing: bool = False
    host: str = "127.0.0.1"
    port: int = 5000
    secret_key: str = "dev-secret-key-change-in-production"

    @classmethod
    def from_env(cls) -> "FlaskConfig":
        """Create configuration from environment variables."""
        return cls(
            debug=os.getenv("FLASK_DEBUG", "true").lower() == "true",
            testing=os.getenv("FLASK_TESTING", "false").lower() == "true",
            host=os.getenv("FLASK_HOST", "127.0.0.1"),
            port=int(os.getenv("FLASK_PORT", "5000")),
            secret_key=os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
        )


@dataclass(frozen=True)
class Config:
    """Main application configuration."""

    database: DatabaseConfig
    api: APIConfig
    gemini: GeminiConfig
    flask: FlaskConfig

    @property
    def base_dir(self) -> Path:
        """Get base directory of the project."""
        return Path(__file__).parent.parent


@lru_cache(maxsize=1)
def get_config() -> Config:
    """
    Get application configuration (singleton).

    Returns:
        Config: Application configuration instance
    """
    return Config(
        database=DatabaseConfig(),
        api=APIConfig(),
        gemini=GeminiConfig(),
        flask=FlaskConfig.from_env()
    )
