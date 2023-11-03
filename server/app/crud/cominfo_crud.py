from typing import List
from datetime import datetime

from sqlalchemy.orm import Session

from app.schemas.cominfo_schema import ComInfoCreate, ComInfo, ComInfoRTCreate, ComInfoRT
from app.models import cominfo_model as model


class CominfoCRUD:
    """
    Cominfo Model에 대한 CURD 구현 클래스
    """

    def __init__(self, session: Session):
        """
        생성자
        :param session: DB Session 객체
        """
        self.session = session

    def create(self, cominfo: ComInfoCreate) -> model.ComInfo:
        """
        ComInfo 객체 생성
        :param cominfo: 추가하려는 ComInfo 객체
        :return: model.ComInfo
        """
        insert_data = model.ComInfo(**dict(cominfo))
        self.session.add(insert_data)
        self.session.commit()
        self.session.refresh(insert_data)
        return insert_data

    def get_by_datetime(self, host_id: int, start_dt: datetime, end_dt: datetime) -> List[model.ComInfo]:
        """
        시작 날짜 ~ 종료 날짜 사이의 ComInfo 객체를 가져오기
        :param host_id: Host ID 값
        :param start_dt: 시작 날짜/시간
        :param end_dt: 종료 날짜/시간
        :return: List[model.ComInfo]
        """
        query = self.session.query(model.ComInfo).filter(model.ComInfo.host_id == host_id)

        if start_dt:
            query = query.filter(model.ComInfo.make_datetime >= start_dt)

        if end_dt:
            query = query.filter(model.ComInfo.make_datetime <= end_dt)

        return query.all()

    def get_multiline(self, host_id: int, skip: int = 0, limit: int = 1000) -> List[model.ComInfo]:
        """
        ComInfo 객체를 가져오기
        :param host_id: Host ID 값
        :param skip: 넘기려는 데이터 Row
        :param limit: 가져오려는 Row
        :return: List[model.ComInfo]
        """
        return (self.session
                .query(model.ComInfo)
                .filter(model.ComInfo.host_id == host_id)
                .offset(skip)
                .limit(limit)
                .all())


class CominfoRtCRUD:
    """
    CominfoRT(Real-Time) Model에 대한 CURD 구현 클래스
    """

    def __init__(self, session: Session):
        self.session = session

    def create(self, cominfo: ComInfoRTCreate) -> model.ComInfoRT:
        """
        ComInfoRT 객체를 생성
        :param cominfo: 생성하려는 ComInfoRT 객체
        :return: model.ComInfoRT
        """
        create_data = model.ComInfoRT(**dict(cominfo))
        self.session.add(create_data)
        self.session.commit()
        self.session.refresh(create_data)
        return create_data

    def get(self, host_id: int) -> model.ComInfoRT:
        """
        Host ID에 해당하는 ComInfoRT 데이터 읽기
        :param host_id: Host ID 값
        :return: model.ComInfoRT
        """
        return (self.session
                .query(model.ComInfoRT)
                .filter(model.ComInfoRT.host_id == host_id)
                .first())

    def update(self, origin: ComInfoRT, update: ComInfoRTCreate) -> model.ComInfoRT:
        """
        ComInfoRt 객체 수정
        :param origin: 원본 데이터
        :param update: 수정하려는 데이터
        :return: model.ComInfo
        """
        update_data = dict(update)
        for key, value in update_data.items():
            setattr(origin, key, value)

        self.session.add(origin)
        self.session.commit()
        self.session.refresh(origin)
        return origin
