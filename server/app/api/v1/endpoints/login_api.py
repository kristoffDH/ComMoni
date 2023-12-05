from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.crud.user_crud import UserCRUD
from app.schemas.user_schema import UserVerify

from app.schemas.token_schema import Token, TokenData
from app.core.token import JwtTokenType, create_token, get_current_user

from app.core.return_code import ReturnCode
from app.exception import api_exception
from app.exception.crud_exception import CrudException

from app.core.log import logger

router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_token(
        *,
        db: Session = Depends(get_db),
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
        logger.error(f"[login]Err : {err}")
        if err.return_code == ReturnCode.USER_NOT_FOUND:
            raise api_exception.UserNotFound(user_id=form_data.username)
        elif err.return_code == ReturnCode.USER_IS_DELETED \
                or err.return_code == ReturnCode.USER_PW_INVALID:
            raise api_exception.Unauthorized()
        else:
            raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    access_token = create_token(user_id=user.user_id, token_type=JwtTokenType.ACCESS)
    refresh_token = create_token(user_id=user.user_id, token_type=JwtTokenType.REFRESH)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh-token", response_model=Token)
def refresh_access_token(
        *,
        db: Session = Depends(get_db),
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
    else:
        logger.info("refresh toekn 유효기간 남음")
        refresh_token = None

    access_token = create_token(user_id=token_data.user_id, token_type=JwtTokenType.ACCESS)
    return Token(access_token=access_token, refresh_token=refresh_token)
