from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

postfix = "/.env"
path = Path(str(Path().absolute()) + postfix)  # This peace of code needed for run configurations and Current file in
while not path.is_file():                         # Pycharm
    path = Path(str(path.parent.parent) + postfix)
print(path)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=path)
    host: str
    port: int


settings = Settings()
