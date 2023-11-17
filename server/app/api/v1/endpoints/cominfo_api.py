from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.cominfo_schema import ComInfoCreate, ComInfo, ComInfoGet
from app.schemas.cominfo_schema import ComInfoRT
from app.schemas.commange_schema import ComManageByHost
from app.crud.cominfo_crud import CominfoCRUD, CominfoRtCRUD
from app.crud.commanage_crud import CommanageCRUD

from app.exception import api_exception
from app.crud.return_code import ReturnCode

from app.core.log import logger

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_cominfo(
        *,
        db: Session = Depends(get_db),
        cominfo: ComInfoCreate
) -> None:
    """
    ComInfo 객체 추가
    :param db: db Session
    :param cominfo: 추가하려는 ComInfo 객체
    :return: ComInfoCreate 스키마
    """
    if not CommanageCRUD(db).get(commanage=ComManageByHost(host_id=cominfo.host_id)):
        raise api_exception.HostNotFound(host_id=cominfo.host_id)

    if CominfoCRUD(db).create(cominfo=cominfo) == ReturnCode.DB_CREATE_ERROR:
        logger.error(f"ComInfo Create Fail. cominfo : {cominfo}")
        raise api_exception.ServerError(f"Server Error. ErrorCode : {ReturnCode.DB_CREATE_ERROR}")


@router.get("/", response_model=list[ComInfo])
def get_cominfos(
        *,
        db: Session = Depends(get_db),
        host_id: int,
        skip: int = 0,
        limit: int = 50,
        start_dt: Optional[datetime] = None,
        end_dt: Optional[datetime] = None
) -> List[ComInfo]:
    """
    ComInfo 값 가져오기
    :param db: db Session
    :param host_id: Host Id 값
    :param skip: 넘기려는 데이터 Row
    :param limit: 가져오려는 Row
    :param start_dt: 시작 날짜/시간
    :param end_dt: 종료 날짜/시간
    :return: List[ComInfoGet] 스키마
    """
    if start_dt or end_dt:
        cominfos = CominfoCRUD(db).get_by_datetime(cominfo=ComInfoGet(host_id=host_id),
                                                   start_dt=start_dt, end_dt=end_dt)
    else:
        cominfos = CominfoCRUD(db).get_multiline(cominfo=ComInfoGet(host_id=host_id),
                                                 skip=skip, limit=limit)

    if not cominfos:
        raise api_exception.ItemNotFound()

    return cominfos


@router.put("/realtime", status_code=status.HTTP_204_NO_CONTENT)
def put_cominfo_realtime(
        *,
        db: Session = Depends(get_db),
        cominfo: ComInfoRT
) -> None:
    """
    CominfoRT(Real-Time) 값 추가 또는 수정
    :param db: db Session
    :param cominfo: 추가하려는 ComInfo 객체
    :return: None
    """
    if not CominfoRtCRUD(db).get(cominfo=ComInfoRT(host_id=cominfo.host_id)):
        if CominfoRtCRUD(db).create(cominfo=cominfo) == ReturnCode.DB_CREATE_ERROR:
            logger.error(f"ComInfo Create Fail. cominfo : {cominfo}")
            raise api_exception.ServerError(f"Server Error. ErrorCode : {ReturnCode.DB_CREATE_ERROR}")
    else:
        if CominfoRtCRUD(db).update(update_data=cominfo) == ReturnCode.DB_UPDATE_ERROR:
            logger.error(f"ComInfo Update Fail. cominfo : {cominfo}")
            raise api_exception.ServerError(f"Server Error. ErrorCode : {ReturnCode.DB_UPDATE_ERROR}")


@router.get("/realtime/{host_id}", response_model=ComInfoRT)
def get_cominfo_realtime(
        *,
        db: Session = Depends(get_db),
        host_id: int
) -> ComInfoRT:
    """
    CominfoRT(Real-Time) 값 가져오기
    :param db: ㅇb Session
    :param host_id: Host ID 값
    :return: ComInfoRT 스키마
    """
    if cominfo_rt := CominfoRtCRUD(db).get(cominfo=ComInfoRT(host_id=host_id)):
        return cominfo_rt
    else:
        raise api_exception.HostNotFound(host_id == host_id)
