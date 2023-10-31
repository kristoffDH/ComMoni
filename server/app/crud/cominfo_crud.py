from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.schemas.cominfo_schema import ComInfoCreate, ComInfo
from app.models import cominfo_model as model


def create_cominfo(db: Session, cominfo: ComInfoCreate) -> model.ComInfo:
    """
    coninfo 생성
    :param db: db 객체
    :param cominfo: 추가하려는 데이터
    :return:
    """
    db_data = model.ComInfo(**dict(cominfo))
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_multi_cominfo(db: Session, host_id: int, skip: int = 0, limit: int = 1000) -> List[model.ComInfo]:
    """
    cominfo 데이터를 범위를 지정해서 가져오는 메서드
    :param db: db 객체
    :param host_id: host 아이디
    :param skip: 시작 인덱스
    :param limit: 가져올 범위
    :return: List[ComInfo]
    """
    return (db
            .query(model.ComInfo)
            .filter(model.ComInfo.host_id == host_id)
            .offset(skip)
            .limit(limit)
            .all())


def get_cominfo_by_datetime(db: Session, host_id: int, start_dt: datetime, end_dt: datetime) -> Optional[ComInfo]:
    """
    cominfo와 정확하게 일치하는 데이터를 읽기
    :param db: db 객체
    :param host_id : 호스트 아이디
    :param start_dt : 시작 날짜/시간
    :param end_dt : 종료 날짜/시간
    :return: ComInfo 객체
    """
    return (db
            .query(model.ComInfo)
            .filter(model.ComInfo.host_id == host_id)
            .filter(model.ComInfo.make_datetime >= start_dt)
            .filter(model.ComInfo.make_datetime <= end_dt)
            .all())


def create_cominfo_rt(db: Session, cominfo: ComInfo) -> model.ComInfo:
    """
    coninfo(실시간용) 생성
    :param db: db 객체
    :param cominfo: 추가하려는 데이터
    :return:
    """
    db_data = model.ComInfoRT(**dict(cominfo))
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_cominfo_rt(db: Session, host_id: int) -> model.ComInfo:
    """
    coninfo(실시간용) 데이터 가져오기
    :param db: db 객체
    :param cominfo: 추가하려는 데이터
    :return:
    """
    return (db
            .query(model.ComInfoRT)
            .filter(model.ComInfoRT.host_id == host_id)
            .first())


def update_cominfo_rt(db: Session, origin: ComInfo, update: ComInfo) -> ComInfo:
    """
    coninfo(실시간용) 생성
    :param db: db 객체
    :param cominfo: 업데이트하려는 데이터
    :return:
    """
    update_data = dict(update)
    for key, value in update_data.items():
        setattr(origin, key, value)

    db.add(origin)
    db.commit()
    db.refresh(origin)
    return origin
