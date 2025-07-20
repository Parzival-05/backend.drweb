from pathlib import Path
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings

FILE_STORAGE_PATH = Path.cwd() / "store"


class DBConnConfig(BaseSettings):
    USER: str = Field(validation_alias="POSTGRES_USER")
    PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD")
    HOST: str = Field(validation_alias="POSTGRES_HOST")
    PORT: int = Field(validation_alias="POSTGRES_PORT")

    def pg_dsn(self, name) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
            path=name,
        )


class LogConfig(BaseSettings):
    LOG_FILE: str = Field(validation_alias="LOG_FILE")


class StorageConfig(BaseSettings):
    BASE_PATH: str = "store"


class BaseConfig(BaseSettings):
    """Base configuration."""

    DEBUG: bool = False
    TESTING: bool = False
    DB_CONN: DBConnConfig = DBConnConfig()  # type: ignore
    LOG_CONFIG: LogConfig = LogConfig()  # type: ignore
    STORAGE: StorageConfig = StorageConfig()

    FLASK_ENV: str = Field(validation_alias="FLASK_ENV")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return self.DB_CONN.pg_dsn(self.FLASK_ENV).encoded_string()


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG: bool = True


class TestingConfig(BaseConfig):
    """Testing configuration."""

    DEBUG: bool = True
    TESTING: bool = True


class ProductionConfig(BaseConfig):
    """Production configuration."""

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
