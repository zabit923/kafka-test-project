from pathlib import Path
from typing import Literal

from environs import Env
from pydantic import BaseModel
from pydantic_settings import BaseSettings


env = Env()
env.read_env()


DEBUG = env.bool("DEBUG")

BASE_DIR = Path(__file__).parent


LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

DB_USERNAME = env.str("POSTGRES_USER")
DB_PASSWORD = env.str("POSTGRES_PASSWORD")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.int("DB_PORT")
DB_DATABASE = env.str("POSTGRES_DB")


KAFKA_BOOTSTRAP_SERVERS = "kafka:9093"
if DEBUG:
    KAFKA_BOOTSTRAP_SERVERS = "localhost:9093"
KAFKA_TOPIC = "Kafka"


SECRET_KEY = env.str("SECRET_KEY")


class SecretKey(BaseModel):
    secret_key: str = SECRET_KEY


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT


class DbSettings(BaseModel):
    url: str = (
        f"postgresql+asyncpg://"
        f"{DB_USERNAME}:"
        f"{DB_PASSWORD}@"
        f"localhost:"
        f"{DB_PORT}/"
        f"{DB_DATABASE}"
        if DEBUG
        else f"postgresql+asyncpg://"
        f"{DB_USERNAME}:"
        f"{DB_PASSWORD}@"
        f"{DB_HOST}:"
        f"{DB_PORT}/"
        f"{DB_DATABASE}"
    )
    test_url: str = "sqlite+aiosqlite:///test.db"
    echo: bool = True


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    db: DbSettings = DbSettings()
    secret: SecretKey = SecretKey()
    logging: LoggingConfig = LoggingConfig()


settings = Settings()
