from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.commange_schema import ComManageByUser, ComManageByHost
from app.models import commanage_model as model
from app.core.dictionary_util import dictionary_util
from app.crud.return_code import ReturnCode

from app.core.log import logger


class CommanageCRUD:
    """
    Commanage Model에 대한 CURD 구현 클래스
    """

    def __init__(self, session: Session):
        """
        생성자
        :param session: DB Session 객체
        """
        self.session = session

    def create(self, commanage: ComManageByUser) -> (ReturnCode, int):
        """
        ComManage 객체 생성
        :param commanage: 추가하려는 ComManage 객체
        :return: ReturnCode, host_id
        """
        insert_data = model.ComManage(**dict(commanage))
        try:
            self.session.add(insert_data)
            self.session.commit()
            self.session.refresh(insert_data)
        except SQLAlchemyError as err:
            logger.error(f"[ComManage]DB Error : {err}")
            self.session.rollback()
            return ReturnCode.DB_CREATE_ERROR

        return ReturnCode.DB_OK, insert_data.host_id

    def get(self, commanage: ComManageByHost) -> model.ComManage:
        """
        ComManage 객체를 가져오기
        :param commanage: get 요청 객체
        :return: model.ComManage
        """
        return self.session \
            .query(model.ComManage) \
            .filter(model.ComManage.host_id == commanage.host_id) \
            .first()

    def get_all(self, commanage: ComManageByUser) -> List[model.ComManage]:
        """
        User ID에 해당하는 모든 ComManage 객체를 가져오기
        :param commanage: get 요청 객체
        :return: List[model.ComManage]
        """
        return self.session \
            .query(model.ComManage) \
            .filter(model.ComManage.user_id == commanage.user_id) \
            .all()

    def update(self, update_data: ComManageByHost) -> ReturnCode:
        """
        ComManage 객체 수정
        :param update_data: 수정하려는 데이터
        :return: ReturnCode
        """

        # 값이 None인 키 삭제
        filtered_dict = dictionary_util.remove_none(dict(update_data))

        try:
            updated = self.session.query(model.ComManage) \
                .filter(model.ComManage.host_id == update_data.host_id) \
                .update(filtered_dict)
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[ComManage]DB Error : {err}")
            self.session.rollback()
            return ReturnCode.DB_UPDATE_ERROR

        return ReturnCode.DB_OK if updated > 0 else ReturnCode.DB_UPDATE_NONE

    def delete(self, commanage: ComManageByHost) -> ReturnCode:
        """
        ComManage 삭제
        :param commanage: 호스트 아이디가 포함된 삭제 요청 객체
        :return: ReturnCode
        """

        try:
            deleted = self.session.query(model.ComManage) \
                .filter(model.ComManage.host_id == commanage.host_id) \
                .update({'deleted': True})
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[ComManage]DB Error : {err}")
            self.session.rollback()
            return ReturnCode.DB_DELETE_ERROR

        return ReturnCode.DB_OK if deleted > 0 else ReturnCode.DB_DELETE_NONE

    def delete_all(self, commanage: ComManageByUser) -> ReturnCode:
        """
        User ID에 해당하는 모든 ComManage 삭제 처리
        :param commanage: 유저 아이디가 포함된 삭제 요청 객체
        :return: ReturnCode
        """

        try:
            deleted = self.session.query(model.ComManage) \
                .filter(model.ComManage.user_id == commanage.user_id) \
                .update({'deleted': True})
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[ComManage]DB Error : {err}")
            self.session.rollback()
            return ReturnCode.DB_DELETE_ERROR

        return ReturnCode.DB_OK if deleted > 0 else ReturnCode.DB_DELETE_NONE
