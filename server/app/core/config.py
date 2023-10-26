from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_PREFIX_ENDPOINT: str = "/api"
    API_VERSION: str = "/v1"

    USERNAME: str = "kristoff"
    PASSWORD: str = "1234"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "commonidb"
    SQLALCHEMY_DATABASE_URI: str = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    TABLE_ISNT_EXIST: bool = True

    class Config:
        env_file = '.env'


settings = Settings()
