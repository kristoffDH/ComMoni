from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_PREFIX_ENDPOINT: str = "/api"

    class Config:
        env_file = '.env'


settings = Settings()
