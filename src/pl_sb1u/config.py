"""Configuration for pl-sb1u multi-agent system."""

from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        populate_by_name=True,
        env_file=".env",
        env_file_encoding="utf-8",
    )

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", alias="OPENAI_MODEL")
    temperature: float = Field(default=0.1, alias="TEMPERATURE")

    # SB1U specific settings
    team_name: str = Field(default="SpareBank 1 Utvikling", alias="TEAM_NAME")
    language: str = Field(default="no", alias="LANGUAGE")  # 'no' for Norwegian, 'en' for English


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
