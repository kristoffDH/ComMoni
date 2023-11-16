from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.log import logger
from app.db.base import get_db
from app.crud import return_code
from app.crud.commanage_crud import CommanageCRUD
from app.crud.user_crud import UserCRUD
from app.schemas.user_schema import UserGet, UserCreate, UserResponse, UserStatus
from app.schemas.commange_schema import ComManageByUser

from app.exception import api_exception

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
        *,
        db: Session = Depends(get_db),
        user: UserCreate
) -> UserResponse:
    """
    유저 생성
    :param db: db Session
    :param user: 추가하려는 User 객체
    :return: UserResponse
    """
    if UserCRUD(db).get(user=UserGet(user_id=user.user_id)):
        raise api_exception.AlreadyExistedUser(user_id=user.user_id)

    if UserCRUD(db).create(user=user) == return_code.DB_CREATE_ERROR:
        logger.error(f"User Create Fail. user : {user}")
        raise api_exception.ServerError(f"Server Error. ErrorCode : {return_code.DB_CREATE_ERROR}")

    return UserResponse(user_id=user.user_id, user_name=user.user_name)


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(
        *,
        db: Session = Depends(get_db),
        user_id: str
) -> UserResponse:
    """
    User ID 값으로 User 값 가져오기
    :param db: db Session
    :param user_id: 찾으려고 하는 유저 객체
    :return: UserResponse
    """
    user = UserCRUD(db).get(UserGet(user_id=user_id))
    if not user:
        raise api_exception.UserNotFound(user_id=user_id)

    return UserResponse(user_id=user.user_id, user_name=user.user_name)


@router.get("/{user_id}/status", status_code=status.HTTP_200_OK, response_model=UserStatus)
def get_user_status(
        *,
        db: Session = Depends(get_db),
        user_id: str
) -> UserStatus:
    """
    User 상태 정보 확인
    :param db: db Session
    :param user_id: 확인 하려는 유저 아이디
    :return: UserStatus
    """
    user = UserCRUD(db).get(UserGet(user_id=user_id))
    if not user:
        raise api_exception.UserNotFound(user_id=user_id)

    return UserStatus(user_id=user.user_id, user_name=user.user_name, deleted=user.deleted)


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
def update_user(
        *,
        db: Session = Depends(get_db),
        user: UserGet
) -> None:
    """
    User 객체 정보 수정
    :param db: db Session
    :param user: 수정하려는 유저 정보
    :return: None.
    """
    if not UserCRUD(db).get(user=user):
        raise api_exception.UserNotFound(user_id=user.user_id)

    if UserCRUD(db).update(update_data=user) == return_code.DB_UPDATE_ERROR:
        logger.error(f"user[{user.user_id}] : update fail")
        raise api_exception.ServerError(f"Server Error. ErrorCode : {return_code.DB_UPDATE_ERROR}")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        *,
        db: Session = Depends(get_db),
        user_id: str
) -> None:
    """
    User를 삭제
    :param db: db Session
    :param user: 삭제하려는 유저 정보
    :return: None
    """

    if not UserCRUD(db).get(user=UserGet(user_id=user_id)):
        raise api_exception.UserNotFound(user_id=user_id)

    # User ID 에 해당하는 ComManage 전부 삭제 처리
    if CommanageCRUD(db).delete_all(commanage=ComManageByUser(user_id=user_id)) == return_code.DB_DELETE_ERROR:
        logger.error(f"Commanage Delete fail. user_id : {user_id}")
        raise api_exception.ServerError(f"Server Error. ErrorCode : {return_code.DB_DELETE_ERROR}")

    # user delete
    result = UserCRUD(db).delete(user=UserGet(user_id=user_id))
    if result == return_code.DB_DELETE_ERROR:
        logger.error(f"user[{user_id}] : delete fail")
        raise api_exception.ServerError(f"Server Error. ErrorCode : {return_code.DB_DELETE_ERROR}")
