from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class ServiceSettings(BaseSettings):
    service_name: str = "API for prototyper"
    service_description: str = "Prototyper API"

    mode: str = os.environ.get("MODE", "DEV")

    postgres_url: str = os.environ.get("DB_URL", "locahost")
    postgres_echo: bool = bool(os.environ.get("DB_ECHO", False))


settings = ServiceSettings()


class RedisSettings(BaseSettings):
    address: str = "redis"
    port: str = "6379"

    model_config = SettingsConfigDict(env_prefix="redis_")


redis_settings = RedisSettings()
