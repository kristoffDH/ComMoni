from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.crud.user_crud import UserCRUD
from app.schemas.user_schema import UserVerify

from app.schemas.token_schema import Token
from app.core.token import create_token, JwtTokenType

from app.core.return_code import ReturnCode
from app.exception import api_exception
from app.exception.crud_exception import CrudException

from app.core.log import logger

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_token(
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
    return Token(access_token=access_token)
