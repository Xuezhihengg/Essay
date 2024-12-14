from pydantic_settings import BaseSettings
from .log_config import LOGGING_CONFIG

class Settings(BaseSettings):
    VERSION: str = "0.1.0"
    APP_TITLE: str = "EssayGenie基于大模型的智能作文教学体"
    PROJECT_NAME: str = "EssayGenie"
    APP_DESCRIPTION: str = "基于大模型的智能作文教学体"
    LOGGING_CONFIG: dict = LOGGING_CONFIG
    

settings = Settings()