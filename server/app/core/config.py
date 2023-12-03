from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_PREFIX_ENDPOINT: str = "/api"
    API_VERSION: str = "/v1"

    # Database
    USERNAME: str = "kristoff"
    PASSWORD: str = "1234"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "commonidb"
    SQLALCHEMY_DATABASE_URI: str = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # JWT
    SECRET_KEY: str = "0548a115e749bd446115d6c05e95838b2f7b47568e110186e0fe81fca376e19d"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20  # minute
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 15  # date

    # Redis
    REDIS_IP: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB_NUM: int = 0

    class Config:
        env_file = '.env'


settings = Settings()
