from datetime import datetime, timedelta

import redis.exceptions
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.crud.user_crud import UserCRUD
from app.crud.commanage_crud import CommanageCRUD
from app.schemas.user_schema import UserVerify
from app.schemas.commange_schema import ComManageByHost

from app.schemas.token_schema import Token, TokenData
from app.core.token import JwtTokenType, create_token, get_current_user

from app.core.return_code import ReturnCode
from app.exception import api_exception
from app.exception.crud_exception import CrudException

from app.core.log import logger
from app.core.config import settings
from app.core.token import redis_con

router = APIRouter()


@router.post("/login", response_model=Token)
def login_for_token(
        *,
        db: Session = Depends(get_db),
        host_id: int = 0,
        form_data=Depends(OAuth2PasswordRequestForm)
):
    """
    login 및 토큰 생성
    :param db: db session
    :param form_data: OAuth2 요청 form
    :return: Token 스키마
    """
    try:
        user = UserCRUD(db).authenticate_user(
            UserVerify(user_id=form_data.username, user_pw=form_data.password))
    except CrudException as err:
        logger.error(f"[login]user crud err : {err}")
        if err.return_code == ReturnCode.USER_NOT_FOUND:
            raise api_exception.UserNotFound(user_id=form_data.username)
        elif err.return_code == ReturnCode.USER_IS_DELETED \
                or err.return_code == ReturnCode.USER_PW_INVALID:
            raise api_exception.Unauthorized()
        else:
            raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if host_id != 0:
        try:
            result = CommanageCRUD(db).get(commanage=ComManageByHost(host_id=host_id))
        except CrudException as err:
            logger.error(f"[login]commanage crud err : {err}")
            raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

        if not result:
            raise api_exception.HostNotFound(host_id=host_id)

    access_token = create_token(user_id=user.user_id, host_id=host_id, token_type=JwtTokenType.ACCESS)
    refresh_token = create_token(user_id=user.user_id, host_id=host_id, token_type=JwtTokenType.REFRESH)

    # refresh 저장
    try:
        redis_con.set(name=user.user_id, value=refresh_token)
    except redis.exceptions.RedisError as err:
        logger.error(f"[login]redis : {err}")
        raise api_exception.ServerError(f"Server Error. redis error")

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/refresh-token", response_model=Token)
def refresh_access_token(
        *,
        token_data: TokenData = Depends(get_current_user)
) -> Token:
    """

    :param db: db session
    :param token_data: 토큰 정보
    :return: Token
    """
    logger.info(f"token expire date : {datetime.fromtimestamp(token_data.expire)}")

    if token_data.expire < (datetime.utcnow() + timedelta(days=2)).timestamp():
        logger.info("refresh token 재발급")
        refresh_token = create_token(user_id=token_data.user_id, token_type=JwtTokenType.REFRESH)

        try:
            redis_con.set(name=token_data.user_id, value=refresh_token)
        except redis.exceptions.RedisError as err:
            logger.error(f"[login]redis : {err}")
            raise api_exception.ServerError(f"Server Error. redis error")
    else:
        logger.info("refresh toekn 유효기간 남음")
        refresh_token = None

    access_token = create_token(user_id=token_data.user_id, token_type=JwtTokenType.ACCESS)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/logout")
def logout(
        *,
        token_data: TokenData = Depends(get_current_user)
) -> JSONResponse:
    """
    logout
    :param db: db session
    :param token_data: 토큰 정보
    :return: JSONResponse
    """
    try:
        redis_con.delete(token_data.user_id)
        redis_con.setex(name=f"{token_data.user_id}_logout", value=token_data.token,
                        time=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    except redis.exceptions.RedisError as err:
        logger.error(f"[login]redis : {err}")
        raise api_exception.ServerError(f"Server Error. redis error")

    return JSONResponse(content={
        "message": "logout success"
    })
