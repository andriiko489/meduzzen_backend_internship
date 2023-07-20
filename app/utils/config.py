from pydantic_settings import BaseSettings, SettingsConfigDict
import dotenv

found_dotenv = dotenv.find_dotenv('.env')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=found_dotenv)
    host: str
    port: int
    database_url: str
    test_database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    domain: str
    api_audience: str
    algorithms: str
    issuer: str

settings = Settings()
