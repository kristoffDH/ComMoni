from datetime import datetime, timedelta
from enum import Enum

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.schemas.token_schema import TokenData

from app.exception.api_exception import TokenInvalidate

from app.core.config import settings
from app.core.log import logger

import redis

redis_con = redis.StrictRedis(host=settings.REDIS_IP, port=settings.REDIS_PORT,
                              db=settings.REDIS_DB_NUM)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/token")


class JwtTokenType(Enum):
    """
    token 타입 정의를 위한 enum class
    """
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"

    def __str__(self):
        return str(self.value)


def create_token(user_id: str, host_id: int, token_type: JwtTokenType) -> str:
    """
    토큰 생성
    :param user_id: 토큰을 발행할 유저 아이디
    :param expires_delta: 만료 기간
    :param host_id: host 구분을 위한 값
    :param token_type: 토큰 타입
    :return:
    """
    if token_type == JwtTokenType.ACCESS:
        add_expire_timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        add_expire_timedelta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + add_expire_timedelta
    to_encode = {"exp": expire, "type": str(token_type),
                 "user_id": str(user_id), "host_id": host_id}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    jwt 토큰에서 현재 사용자 확인
    :param token: jwt 토큰
    :return: UserGet
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        expire = payload.get("exp")
        host_id = payload.get("host_id")

        if not user_id:
            logger.error("[token] user_id is empty in token")
            raise TokenInvalidate("user_id empty")

        if redis_con.get(f"{user_id}_logout"):
            logger.error("[token] token is already logout")
            raise TokenInvalidate("token is already logout")

        return TokenData(token=token, user_id=user_id, expire=expire, host_id=host_id)
    except JWTError as err:
        logger.error(f"[token] jwt error : {err}")
        raise TokenInvalidate(str(err))
