from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.cominfo.schema import ComInfoCreate, ComInfo, ComInfoGet
from app.api.cominfo.schema import ComInfoRTGet
from app.api.cominfo.service import CominfoService, CominfoRTService

from app.api.auth.service import verify_agent_token, verify_access_token

API_VERSION = "v1"
API_NAME = "cominfo"

cominfo_router = APIRouter(prefix=f"/{API_VERSION}/{API_NAME}")


@cominfo_router.post("/",
                     status_code=status.HTTP_201_CREATED,
                     dependencies=[Depends(verify_agent_token)])
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
    return CominfoService(db=db).create(cominfo=cominfo)


@cominfo_router.get("/{host_id}",
                    status_code=status.HTTP_200_OK,
                    response_model=list[ComInfo],
                    dependencies=[Depends(verify_access_token)])
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
    return CominfoService(db=db).get(host_id=host_id,
                                     skip=skip,
                                     limit=limit,
                                     start_dt=start_dt,
                                     end_dt=end_dt)


@cominfo_router.put("/realtime",
                    status_code=status.HTTP_200_OK,
                    dependencies=[Depends(verify_agent_token)])
def put_cominfo_realtime(
        *,
        db: Session = Depends(get_db),
        cominfo: ComInfoRTGet
) -> JSONResponse:
    """
    CominfoRT(Real-Time) 값 추가 또는 수정
    :param db: db Session
    :param cominfo: 추가하려는 ComInfo 객체
    :return: JSONResponse
    """
    CominfoRTService(db=db).put(cominfo_rt=cominfo)
    return JSONResponse(content={"message": "success"})


@cominfo_router.get("/realtime/{host_id}",
                    status_code=status.HTTP_200_OK,
                    response_model=ComInfoRTGet,
                    dependencies=[Depends(verify_access_token)])
def get_cominfo_realtime(
        *,
        db: Session = Depends(get_db),
        host_id: int,
) -> ComInfoRTGet:
    """
    CominfoRT(Real-Time) 값 가져오기
    :param db: ㅇb Session
    :param host_id: Host ID 값
    :return: ComInfoRT 스키마
    """
    return CominfoRTService(db=db).get(host_id=host_id)
