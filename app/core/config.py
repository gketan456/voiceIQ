from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        case_sensitive = False,
    )
    #App
    app_name: str = "VoiceIQ"
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    #AWS
    aws_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    

    #Bedrock
    bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"

@lru_cache
def get_settings() -> Settings:
    return Settings()