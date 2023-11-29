from datetime import datetime, timedelta
from typing import Union, Any
from enum import Enum

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.schemas.user_schema import UserGet
from app.exception.api_exception import CredentialsError

from app.core.config import settings
from app.core.log import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access_token")


class JwtTokenType(Enum):
    """
    token 타입 정의를 위한 enum class
    """
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"

    def __str__(self):
        return str(self.value)


def create_token(user_id: str, token_type: JwtTokenType) -> str:
    """
    토큰 생성
    :param user_id: 토큰을 발행할 유저 아이디
    :param expires_delta: 만료 기간
    :param token_type: 토큰 타입
    :return:
    """
    if token_type == JwtTokenType.ACCESS:
        add_expire_timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        add_expire_timedelta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + add_expire_timedelta
    to_encode = {"exp": expire, "type": str(token_type), "user_id": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserGet:
    """
    jwt 토큰에서 현재 사용자 확인
    :param token: jwt 토큰
    :return: UserGet
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("user_id")

        if user_id is None:
            logger.error(f"[toekn] {user_id} is empty in token")
            raise CredentialsError()

        return UserGet(user_id=user_id)
    except JWTError as err:
        logger.error(f"[toekn] jwt error : {err}")
        raise CredentialsError()
