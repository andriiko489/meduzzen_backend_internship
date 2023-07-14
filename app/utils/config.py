from pydantic_settings import BaseSettings, SettingsConfigDict
import dotenv

found_dotenv = dotenv.find_dotenv('.env')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=found_dotenv)
    host: str
    port: int
    database_url: str


settings = Settings()
