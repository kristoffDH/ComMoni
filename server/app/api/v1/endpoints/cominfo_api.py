from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.cominfo_schema import ComInfoCreate, ComInfo, ComInfoGet
from app.schemas.cominfo_schema import ComInfoRT
from app.schemas.commange_schema import ComManageByHost
from app.crud.cominfo_crud import CominfoCRUD, CominfoRtCRUD
from app.crud.commanage_crud import CommanageCRUD

from app.exception import api_exception
from app.exception.crud_exception import CrudException

from app.core.log import logger

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_cominfo(
        *,
        db: Session = Depends(get_db),
        cominfo: ComInfoCreate
) -> ComInfoGet:
    """
    ComInfo 객체 추가
    :param db: db Session
    :param cominfo: 추가하려는 ComInfo 객체
    :return: ComInfoGet 스키마
    """
    try:
        result = CommanageCRUD(db).get(commanage=ComManageByHost(host_id=cominfo.host_id))
    except CrudException as err:
        logger.error("[cominfo api]commanage get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if not result:
        raise api_exception.HostNotFound(host_id=cominfo.host_id)

    try:
        created_cominfo = CominfoCRUD(db).create(cominfo=cominfo)
    except CrudException as err:
        logger.error("[cominfo api]cominfo create error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    return ComInfoGet(host_id=created_cominfo.host_id)


@router.get("/{host_id}", status_code=status.HTTP_200_OK, response_model=list[ComInfo])
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
    try:
        if start_dt or end_dt:
            cominfos = CominfoCRUD(db).get_by_datetime(cominfo=ComInfoGet(host_id=host_id),
                                                       start_dt=start_dt, end_dt=end_dt)
        else:
            cominfos = CominfoCRUD(db).get_multiline(cominfo=ComInfoGet(host_id=host_id),
                                                     skip=skip, limit=limit)
    except CrudException as err:
        logger.error("[cominfo api]cominfo get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if not cominfos:
        raise api_exception.ItemNotFound()

    return cominfos


@router.put("/realtime", status_code=status.HTTP_200_OK)
def put_cominfo_realtime(
        *,
        db: Session = Depends(get_db),
        cominfo: ComInfoRT
) -> JSONResponse:
    """
    CominfoRT(Real-Time) 값 추가 또는 수정
    :param db: db Session
    :param cominfo: 추가하려는 ComInfo 객체
    :return: JSONResponse
    """
    try:
        result = CominfoRtCRUD(db).get(cominfo=ComInfoRT(host_id=cominfo.host_id))
    except CrudException as err:
        logger.error("[cominfoRT api]cominfort get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if not result:
        try:
            created = CominfoRtCRUD(db).create(cominfo=cominfo)
        except CrudException as err:
            logger.error("[cominfoRT api]cominfort create error : " + str(err.return_code))
            raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

        return JSONResponse(content={"message": f"host[{created.host_id}] create success"})
    else:
        try:
            CominfoRtCRUD(db).update(update_data=cominfo)
        except CrudException as err:
            logger.error("[cominfoRT api]cominfort update error : " + str(err.return_code))
            raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

        return JSONResponse(content={"message": "update success"})


@router.get("/realtime/{host_id}", status_code=status.HTTP_200_OK, response_model=ComInfoRT)
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
    try:
        result = CominfoRtCRUD(db).get(cominfo=ComInfoRT(host_id=host_id))
    except CrudException as err:
        logger.error("[cominfoRT api]cominfort get error : " + str(err.return_code))
        raise api_exception.ServerError(f"Server Error. ErrorCode : {err.return_code}")

    if not result:
        raise api_exception.HostNotFound(host_id == host_id)

    return result
