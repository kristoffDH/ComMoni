from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.log import logger
from app.db.base import get_db
from app.crud import return_code
from app.crud.commanage_crud import CommanageCRUD
from app.crud.user_crud import UserCRUD
from app.schemas.user_schema import UserCreate, UserUpdate, UserDelete, UserResponse

from app.exception import api_exception

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
        *,
        db: Session = Depends(get_db),
        user: UserCreate
) -> None:
    """
    유저 생성
    :param db: db Session
    :param user: 추가하려는 User 객체
    :return: None
    """
    if UserCRUD(db).get(user_id=user.user_id):
        raise api_exception.AlreadyExistedUser(user_id=user.user_id)

    if UserCRUD(db).create(user=user) == return_code.DB_CREATE_ERROR:
        logger.error(f"User Create Fail. user_id : {user.user_id}")
        raise api_exception.ServerError(f"Server Error. ErrorCode : {return_code.DB_CREATE_ERROR}")


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(
        *,
        db: Session = Depends(get_db),
        user_id: str
) -> UserResponse:
    """
    User ID 값으로 User 값 가져오기
    :param db: db Session
    :param user_id: 찾으려고 하는 유저 아이디
    :return: UserResponse
    """
    user = UserCRUD(db).get(user_id=user_id)

    if not user:
        raise api_exception.UserNotFound(user_id=user_id)

    if user.deleted:
        raise api_exception.DeletedUser(user_id=user_id)

    return UserResponse(user_id=user.user_id, user_name=user.user_name)


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
def update_user(
        *,
        db: Session = Depends(get_db),
        user: UserUpdate
) -> None:
    """
    User 객체 정보 수정
    :param db: db Session
    :param user: 수정하려는 유저 정보
    :return: None.
    """

    result = UserCRUD(db).update(update_data=user)
    if result == return_code.DB_UPDATE_NONE:
        raise api_exception.UserNotFound(user_id=user.user_id)
    elif result == return_code.DB_UPDATE_ERROR:
        logger.error(f"{user.user_id} : update fail")
        raise api_exception.ServerError(f"Server Error. ErrorCode : {return_code.DB_UPDATE_ERROR}")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        *,
        db: Session = Depends(get_db),
        user: UserDelete
) -> None:
    """
    User를 삭제
    :param db: db Session
    :param user: 삭제하려는 유저 정보
    :return: None
    """

    if not UserCRUD(db).get(user_id=user.user_id):
        raise api_exception.UserNotFound(user_id=user.user_id)

    # User ID 에 해당하는 ComManage 전부 삭제 처리
    if CommanageCRUD(db).delete_all(user_id=user.user_id) == return_code.DB_DELETE_ERROR:
        logger.error("Commanage Delete fail. user_id : {user.user_id}")
        raise api_exception.ServerError(f"Server Error. ErrorCode : {return_code.DB_DELETE_ERROR}")

    # user delete
    result = UserCRUD(db).delete(user_id=user.user_id)
    if result == return_code.DB_DELETE_NONE:
        raise api_exception.UserNotFound(user_id=user.user_id)
    elif result == return_code.DB_DELETE_ERROR:
        logger.error(f"{user.user_id} : delete fail")
        raise api_exception.ServerError(f"Server Error. ErrorCode : {return_code.DB_DELETE_ERROR}")
