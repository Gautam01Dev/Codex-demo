from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SmartInvest AI"
    secret_key: str = "change-this-secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    database_url: str = "sqlite:///./smartinvest.db"
    redis_url: str = "redis://localhost:6379/0"

    alpha_vantage_api_key: str | None = None
    news_api_key: str | None = None

    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
