from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_key: str = Field(default="demo-secret-key", alias="API_KEY")

    db_type: str | None = Field(default=None, alias="DB_TYPE")
    db_host: str | None = Field(default=None, alias="DB_HOST")
    db_port: int | None = Field(default=None, alias="DB_PORT")
    db_name: str | None = Field(default=None, alias="DB_NAME")
    db_user: str | None = Field(default=None, alias="DB_USER")
    db_password: str | None = Field(default=None, alias="DB_PASSWORD")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()