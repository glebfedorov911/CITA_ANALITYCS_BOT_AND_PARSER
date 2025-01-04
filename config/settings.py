from pydantic_settings import BaseSettings
from pydantic import BaseModel

from .config import URL, ECHO


class DataBaseSettings(BaseModel):
    URL: str = URL
    ECHO: str = ECHO

class Settings(BaseSettings):
    db_settings: DataBaseSettings = DataBaseSettings()

settings = Settings()