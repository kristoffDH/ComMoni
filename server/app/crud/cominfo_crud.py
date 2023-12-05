from typing import List
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.cominfo_schema import ComInfoCreate, ComInfoGet, ComInfoRT
from app.models import cominfo_model as model

from app.core.return_code import ReturnCode
from app.exception.crud_exception import CrudException

from app.core.log import logger


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
        try:
            self.session.add(insert_data)
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[ComInfo]DB Error : {err}")
            self.session.rollback()
            raise CrudException(return_code=ReturnCode.DB_CREATE_ERROR)

        return insert_data

    def get_by_datetime(self, cominfo: ComInfoGet, start_dt: datetime = None, end_dt: datetime = None) -> List[
        model.ComInfo]:
        """
        시작 날짜 ~ 종료 날짜 사이의 ComInfo 객체를 가져오기
        :param cominfo: Host ID 값이 포함된 객체
        :param start_dt: 시작 날짜/시간
        :param end_dt: 종료 날짜/시간
        :return: List[model.ComInfo]
        """
        try:
            query = self.session.query(model.ComInfo) \
                .filter(model.ComInfo.host_id == cominfo.host_id)

            if start_dt:
                query = query.filter(model.ComInfo.make_datetime >= start_dt)

            if end_dt:
                query = query.filter(model.ComInfo.make_datetime <= end_dt)

            return query.all()
        except SQLAlchemyError as err:
            logger.error(f"[ComInfo]DB Error : {err}")
            raise CrudException(return_code=ReturnCode.DB_GET_ERROR)

    def get_multiline(self, cominfo: ComInfoGet, skip: int = 0, limit: int = 1000) -> List[model.ComInfo]:
        """
        ComInfo 객체를 가져오기
        :param cominfo: Host ID 값이 포함된 객체
        :param skip: 넘기려는 데이터 Row
        :param limit: 가져오려는 Row
        :return: List[model.ComInfo]
        """
        try:
            return self.session \
                .query(model.ComInfo) \
                .filter(model.ComInfo.host_id == cominfo.host_id) \
                .offset(skip) \
                .limit(limit) \
                .all()
        except SQLAlchemyError as err:
            logger.error(f"[ComInfo]DB Error : {err}")
            raise CrudException(return_code=ReturnCode.DB_GET_ERROR)


class CominfoRtCRUD:
    """
    CominfoRT(Real-Time) Model에 대한 CURD 구현 클래스
    """

    def __init__(self, session: Session):
        self.session = session

    def create(self, cominfo: ComInfoRT) -> model.ComInfoRT:
        """
        ComInfoRT 객체를 생성
        :param cominfo: 생성하려는 ComInfoRT 객체
        :return: model.ComInfoRT
        """
        insert_data = model.ComInfoRT(**dict(cominfo))
        try:
            self.session.add(insert_data)
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[ComInfoRT]DB Error : {err}")
            self.session.rollback()
            raise CrudException(return_code=ReturnCode.DB_CREATE_ERROR)

        return insert_data

    def get(self, cominfo: ComInfoRT) -> model.ComInfoRT:
        """
        Host ID에 해당하는 ComInfoRT 데이터 읽기
        :param cominfo: Host ID 값이 포함된 객체
        :return: model.ComInfoRT
        """
        try:
            return self.session \
                .query(model.ComInfoRT) \
                .filter(model.ComInfoRT.host_id == cominfo.host_id) \
                .first()
        except SQLAlchemyError as err:
            logger.error(f"[ComInfoRT]DB Error : {err}")
            raise CrudException(return_code=ReturnCode.DB_GET_ERROR)

    def update(self, update_data: ComInfoRT) -> ReturnCode:
        """
        ComInfoRt 객체 수정
        :param update_data: 수정하려는 데이터
        :return: ReturnCode
        """

        try:
            updated = self.session.query(model.ComInfoRT) \
                .filter(model.ComInfoRT.host_id == update_data.host_id) \
                .update(dict(update_data))
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[ComInfoRT]DB Error : {err}")
            self.session.rollback()
            raise CrudException(return_code=ReturnCode.DB_UPDATE_ERROR)

        if updated == 0:
            raise CrudException(return_code=ReturnCode.DB_UPDATE_NONE)

        return ReturnCode.DB_OK
