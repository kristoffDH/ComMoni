from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.crud.commanage_crud import CommanageCRUD
from app.crud.user_crud import UserCRUD
from app.schemas.user_schema import UserGet, UserCreate, UserResponse, UserStatus
from app.schemas.commange_schema import ComManageByUser

from app.crud.return_code import ReturnCode
from app.exception import api_exception
from app.exception.crud_exception import CrudException

from app.core.log import logger

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
    try:
        result = UserCRUD(db).get(user=UserGet(user_id=user.user_id))
    except CrudException as err:
        logger.error("[user api]user get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if result:
        raise api_exception.AlreadyExistedUser(user_id=user.user_id)

    try:
        created_user = UserCRUD(db).create(user=user)
    except CrudException as err:
        logger.error(f"[user api]User create error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    return UserResponse(user_id=created_user.user_id, user_name=created_user.user_name)


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
    try:
        user = UserCRUD(db).get(UserGet(user_id=user_id))
    except CrudException as err:
        logger.error("[user api]user get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

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
    try:
        user = UserCRUD(db).get(UserGet(user_id=user_id))
    except CrudException as err:
        logger.error("[user api]user get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if not user:
        raise api_exception.UserNotFound(user_id=user_id)

    return UserStatus(user_id=user.user_id, user_name=user.user_name, deleted=user.deleted)


@router.put("/", status_code=status.HTTP_200_OK)
def update_user(
        *,
        db: Session = Depends(get_db),
        user: UserGet
) -> JSONResponse:
    """
    User 객체 정보 수정
    :param db: db Session
    :param user: 수정하려는 유저 정보
    :return: JSONResponse
    """
    try:
        result = UserCRUD(db).get(user=user)
    except CrudException as err:
        logger.error("[user api]user get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if not result:
        raise api_exception.UserNotFound(user_id=user.user_id)

    try:
        UserCRUD(db).update(update_data=user)
    except CrudException as err:
        logger.error("[user api]user update error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    return JSONResponse(content={"message": "update success"})


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
        *,
        db: Session = Depends(get_db),
        user_id: str
) -> JSONResponse:
    """
    User를 삭제
    :param db: db Session
    :param user_id: 삭제하려는 유저 아이디
    :return: JSONResponse
    """
    try:
        user = UserCRUD(db).get(user=UserGet(user_id=user_id))
    except CrudException as err:
        logger.error("[user api]user get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if not user:
        raise api_exception.UserNotFound(user_id=user_id)

    try:
        # User ID 에 해당하는 ComManage 전부 삭제 처리
        delete_result = CommanageCRUD(db).delete_all(commanage=ComManageByUser(user_id=user_id))
    except CrudException as err:
        logger.error("[user api]commanage delete_all error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if delete_result == ReturnCode.DB_ALL_DELETE_NONE:
        logger.info("[user api]commanage delete_all is none")

    try:
        # user delete
        UserCRUD(db).delete(user=UserGet(user_id=user_id))
    except CrudException as err:
        logger.error("[user api]user delete error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    return JSONResponse(content={"message": "update success"})
