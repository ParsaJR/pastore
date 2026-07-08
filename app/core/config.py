from enum import Enum
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevels(str,Enum):
    Info = "info"
    Debug = "debug"


    @classmethod
    # Using the missing method i can actually override some custom logic for the
    # enum lookup, after it seemed missing...
    def _missing_(cls, value):
        if isinstance(value, str):
            value = value.lower()

            for member in cls:
                if member.lower() == value:
                    return member

        
        return None




# Envs.
# 1. Can be override at runtime. (Prefix Using "PASTORE_")
# 2. Can be set also by the .env file in the project's root folder. ONLY IN DEVELOPMENT!
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PASTORE_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    ## General
    app_name: str = "Pastore"

    development: bool = False

    ## Database related
    Database_Host: str = "localhost"
    Database_Port: int = 5432  # Postgres uses 5432 by default, for active listen port.
    Database_Password: str = "secret"
    Database_Username: str = "postgres"
    Database_Name: str = "pasted"

    ## JWT Issues
    JWT_Secret: str
    JWT_TTL: int = 604_800

    ## Logs
    LOG_ENABLED: bool = True
    LOG_STRUCTURED: bool = False
    LOG_LOKI_URL: str = ""
    LOG_LEVEL: LogLevels = LogLevels.Debug


settings = Settings()  # pyright: ignore[reportCallIssue]
