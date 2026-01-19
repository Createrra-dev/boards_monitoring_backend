import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """
    Общие настройки приложения.
    """

    model_config = SettingsConfigDict(
        env_file=f"{str(Path(__file__).resolve().parent.parent.parent) + os.sep + '.envs' + os.sep}.app",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_ACCESS_TOKEN_ADMIN_EXPIRE_DAYS: int
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int
    JWT_ALGORITHM: str
    SESSION_SECRET_KEY: str
    ALLOWED_HOSTS_STRING: str
    ORIGINS_STRING: str
    THRESHOLD_SEC: int
    PRODUCTION_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    BOT_TOKEN: str
    GROUP_CHART_ID: int

    @property
    def ALLOWED_HOSTS(self):
        return self.ALLOWED_HOSTS_STRING.split(",")

    @property
    def ORIGINS(self):
        return self.ORIGINS_STRING.split(",")
    
    @property
    def BASE_DIR(self):
        return str(Path(__file__).resolve().parent.parent) + os.sep
    
    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


class PostgresSettings(BaseSettings):
    """
    Настройки Postgresql.
    """

    model_config = SettingsConfigDict(
        env_file=f"{str(Path(__file__).resolve().parent.parent.parent) + os.sep + '.envs' + os.sep}.postgres",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str

    @property
    def DB_URL(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


class LoggingSettings(BaseSettings):
    """
    Настройки логгирования приложения.
    """

    model_config = SettingsConfigDict(
        env_file=f"{str(Path(__file__).resolve().parent.parent.parent) + os.sep + '.envs' + os.sep}.app",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    SERVER_NAME: str
    UDP_HOST: str
    UDP_PORT: int

    @property
    def LOGGING(self):
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {"format": "%(levelname)s %(message)s"},
                "uvicorn_access": {
                    # uvicorn.access форматит поля сам, но можно оставить дефолт
                    "format": "%(levelname)s %(message)s"
                },
            },
            "handlers": {
                "udp": {
                    "level": "INFO",
                    "class": "udp_logger.logger.udp_handler.UDPSyncLoggerHandler",
                    "udp_host": self.UDP_HOST,
                    "udp_port": self.UDP_PORT,
                    "server_name": self.SERVER_NAME,
                },
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                },
            },
            "loggers": {
                # твой прикладной логгер
                "logger": {
                    "handlers": ["udp", "console"],
                    "level": "INFO",
                    "propagate": False,
                },
                # Логи fastapi/uvicorn:
                "uvicorn": {
                    "handlers": ["udp", "console"],
                    "level": "INFO",
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["udp", "console"],
                    "level": "INFO",
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["udp", "console"],
                    "level": "INFO",
                    "propagate": False,
                },
                "fastapi": {
                    "handlers": ["udp", "console"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }


app_settings = AppSettings()
postgres_settings = PostgresSettings()
logging_settings = LoggingSettings()
