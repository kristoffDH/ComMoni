from typing import List, Optional
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.commange_schema import ComManage, ComManageByUser, ComManageByHost, ComManageResponse
from app.schemas.user_schema import UserGet
from app.crud.commanage_crud import CommanageCRUD
from app.crud.user_crud import UserCRUD

from app.exception import api_exception
from app.exception.crud_exception import CrudException

from app.core.log import logger

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_commanage(
        *,
        db: Session = Depends(get_db),
        commanage: ComManageByUser
) -> ComManageResponse:
    """
    ComManage 생성
    :param db: db Session
    :param commanage: 추가하려는 ComManage 객체
    :return: ComManageResponse
    """
    try:
        result = UserCRUD(db).get(UserGet(user_id=commanage.user_id))
    except CrudException as err:
        logger.error("[commanage api]commanage get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if not result:
        raise api_exception.UserNotFound(user_id=commanage.user_id)

    try:
        created_commanage = CommanageCRUD(db).create(commanage=commanage)
    except CrudException as err:
        logger.error("[commanage api]commanage create error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    return ComManageResponse(host_id=created_commanage.host_id)


@router.get("/{host_id}", status_code=status.HTTP_200_OK, response_model=ComManage)
def get_commanage(
        *,
        db: Session = Depends(get_db),
        host_id: Optional[int]
) -> ComManage:
    """
    Host ID로 ComManage 가져오기
    :param db: db Session
    :param host_id: Host ID 값
    :return: ComManage 스키마
    """
    try:
        commanage = ComManageByHost(host_id=host_id)
        result = CommanageCRUD(db).get(commanage=commanage)
    except CrudException as err:
        logger.error("[commanage api]commanage get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if not result:
        raise api_exception.ItemNotFound()

    return result


@router.get("/all/{user_id}", status_code=status.HTTP_200_OK, response_model=list[ComManage])
def get_all_commanage(
        *,
        db: Session = Depends(get_db),
        user_id: Optional[str]
) -> List[ComManage]:
    """
    User ID로 ComManage 가져오기
    :param db: db Session
    :param user_id: User ID 값
    :return: List[ComManage] 스키마
    """
    try:
        commanage = ComManageByUser(user_id=user_id)
        return CommanageCRUD(db).get_all(commanage=commanage)
    except CrudException as err:
        logger.error("[commanage api]commanage get all error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")


@router.put("/", status_code=status.HTTP_200_OK)
def update_commanage(
        *,
        db: Session = Depends(get_db),
        commanage: ComManageByHost
) -> JSONResponse:
    """
    ComManage 객체 수정
    :param db: db Session
    :param commanage: 수정하려는 ComManage 객체
    :return: None
    """
    try:
        result = CommanageCRUD(db).get(commanage=commanage)
    except CrudException as err:
        logger.error("[commanage api]commanage get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if not result:
        raise api_exception.HostNotFound(host_id=commanage.host_id)

    try:
        CommanageCRUD(db).update(update_data=commanage)
    except CrudException as err:
        logger.error("[commanage api]commanage update error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    return JSONResponse(content={"message": "update success"})


@router.delete("/{host_id}", status_code=status.HTTP_200_OK)
def delete_commanage(
        *,
        db: Session = Depends(get_db),
        host_id: int
) -> JSONResponse:
    """
    ComManage 삭제
    :param db: db Session
    :param commanage: 삭제하려는 ComManage 객체
    :return: JSONResponse
    """
    try:
        result = CommanageCRUD(db).get(commanage=ComManageByHost(host_id=host_id))
    except CrudException as err:
        logger.error("[commanage api]commanage get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if not result:
        raise api_exception.HostNotFound(host_id=host_id)

    try:
        CommanageCRUD(db).delete(delete_data=ComManageByHost(host_id=host_id))
    except CrudException as err:
        logger.error("[commanage api]commanage delete error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    return JSONResponse(content={"message": "delete success"})
