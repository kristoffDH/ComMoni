from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_SERVER_URL: str = "http://localhost:8000/api/v1"
    API_SERVER_USER_ID: str = ""
    API_SERVER_USER_PW: str = ""

    REALTIME_SEND_INTERVAL: int = 10
    SEND_INTERVAL: int = 30

    class Config:
        env_file = '.env'


settings = Settings()
