from pathlib import Path

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings

FILE_STORAGE_PATH = Path.cwd() / "store"
TEMP_FILE_STORAGE_PATH = FILE_STORAGE_PATH / "temp"


class DBConnConfig(BaseSettings):
    USER: str = Field(validation_alias="POSTGRES_USER")
    PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD")
    HOST: str = Field(validation_alias="POSTGRES_HOST")
    PORT: int = Field(validation_alias="POSTGRES_PORT")
    DB: str = Field(validation_alias="POSTGRES_DB")

    @property
    def pg_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
            path=self.DB,
        )


class EngineOptions(BaseSettings):
    pool_size: int = Field(validation_alias="POOL_SIZE")
    max_overflow: int = Field(validation_alias="MAX_OVERFLOW")
    pool_pre_ping: bool = Field(validation_alias="POOL_PRE_PING")
    pool_recycle: int = Field(validation_alias="POOL_RECYCLE")
    pool_use_lifo: bool = Field(validation_alias="POOL_USE_LIFO")
    pool_timeout: int = Field(validation_alias="POOL_TIMEOUT")


class LogConfig(BaseSettings):
    LOG_FILE: str = Field(validation_alias="LOG_FILE")


class StorageConfig(BaseSettings):
    BASE_PATH: str = "store"


class BaseConfig(BaseSettings):
    """Base configuration."""

    CONFIG_NAME: str
    DEBUG: bool = False
    TESTING: bool = False

    ENGINE_OPTIONS: EngineOptions = EngineOptions()  # type: ignore
    DB_CONN: DBConnConfig = DBConnConfig()  # type: ignore
    LOG_CONFIG: LogConfig = LogConfig()  # type: ignore
    STORAGE: StorageConfig = StorageConfig()

    FLASK_ENV: str = Field(validation_alias="FLASK_ENV")

    COMPRESS_ALGORITHM: str = "brotli"
    COMPRESS_BROTLI_QUALITY: int = 8

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return self.DB_CONN.pg_dsn.encoded_string()

    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self) -> dict:
        return self.ENGINE_OPTIONS.model_dump()

    @property
    def SQLALCHEMY_TRACK_MODIFICATIONS(self) -> bool:
        return False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    CONFIG_NAME: str = "development"
    DEBUG: bool = True


class TestingConfig(BaseConfig):
    """Testing configuration."""

    CONFIG_NAME: str = "testing"
    DEBUG: bool = True
    TESTING: bool = True


class ProductionConfig(BaseConfig):
    """Production configuration."""

    CONFIG_NAME: str = "production"
    DEBUG: bool = False


def get_config_by_name(config_name) -> BaseConfig:
    """Get config by name"""
    if config_name == "development":
        return DevelopmentConfig()  # type: ignore
    elif config_name == "production":
        return ProductionConfig()  # type: ignore
    elif config_name == "testing":
        return TestingConfig()  # type: ignore
    else:
        return DevelopmentConfig()  # type: ignore
