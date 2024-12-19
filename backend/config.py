from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    db_url: str = f'sqlite:///{BASE_DIR}/app/data/database/sql_app.db' # по этому адресу создатся файл с бд
    USER_BOT_TOKEN: str
    CONF_BOT_TOKEN: str

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}\.env")

settings = Settings() # объект класса настроек