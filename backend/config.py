from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent # путь до корневой папки

class Settings(BaseSettings):
    db_url: str = f'sqlite:///{BASE_DIR}/sql_app.db' # по этому адресу создатся файл с бд

settings = Settings() # объект класса настроек