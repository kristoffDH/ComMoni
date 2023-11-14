from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.commange_schema import ComManage, ComManageByUser, ComManageByHost, ComManageResponse
from app.schemas.user_schema import UserGet
from app.crud.commanage_crud import CommanageCRUD
from app.crud.user_crud import UserCRUD
from app.crud import return_code

from app.exception import api_exception
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
    :return: None
    """
    if not UserCRUD(db).get(UserGet(user_id=commanage.user_id)):
        raise api_exception.UserNotFound(user_id=commanage.user_id)

    result, host_id = CommanageCRUD(db).create(commanage=commanage)

    if result == return_code.DB_CREATE_ERROR:
        logger.error(f"Commanage Create Fail. commanage : {commanage}")
        raise api_exception.ServerError(f"Server Error. ErrorCode : {return_code.DB_CREATE_ERROR}")

    return ComManageResponse(host_id=host_id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ComManage])
def get_commanage(
        *,
        db: Session = Depends(get_db),
        user_id: Optional[str] = None,
        host_id: Optional[int] = None
) -> List[ComManage]:
    """
    User ID 또는 Host ID로 ComManage 가져오기 (User ID와 Host ID 둘 중, 하나는 반드시 필요)
    :param db: db Session
    :param user_id: User ID 값
    :param host_id: Host ID 값
    :return: List[ComManage] 스키마
    """
    if host_id:
        commanage = ComManageByHost(host_id=host_id)
        return [CommanageCRUD(db).get(commanage=commanage)]
    elif user_id:
        commanage = ComManageByUser(user_id=user_id)
        return CommanageCRUD(db).get_all(commanage=commanage)
    else:
        raise api_exception.ItemNotFound()


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
def update_commanage(
        *,
        db: Session = Depends(get_db),
        commanage: ComManageByHost
) -> None:
    """
    ComManage 객체 수정
    :param db: db Session
    :param commanage: 수정하려는 ComManage 객체
    :return: None
    """

    if not CommanageCRUD(db).get(commanage=commanage):
        raise api_exception.HostNotFound(host_id=commanage.host_id)

    if CommanageCRUD(db).update(update_data=commanage) == return_code.DB_UPDATE_ERROR:
        logger.error(f"host[{commanage.host_id}] : update fail")
        raise api_exception.ServerError(f"Server Error. ErrorCode : {return_code.DB_UPDATE_NONE}")


@router.delete("/{host_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_commanage(
        *,
        db: Session = Depends(get_db),
        host_id: int
) -> None:
    """
    ComManage 삭제
    :param db: db Session
    :param commanage: 삭제하려는 ComManage 객체
    :return: None
    """

    if not CommanageCRUD(db).get(commanage=ComManageByHost(host_id=host_id)):
        raise api_exception.HostNotFound(host_id=host_id)

    if CommanageCRUD(db).delete(commanage=ComManageByHost(host_id=host_id)) == return_code.DB_DELETE_ERROR:
        logger.error(f"host[{host_id}] : delete fail")
        raise api_exception.ServerError(f"Server Error. ErrorCode : {return_code.DB_DELETE_ERROR}")
