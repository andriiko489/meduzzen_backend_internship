from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

path = Path(str(Path().absolute()) + "/.env")  # This peace of code needed for run configurations and Current file in
if not path.is_file():                         # Pycharm
    path = Path(str(path.parent.parent) + "/.env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(path))
    host: str
    port: int


settings = Settings()
