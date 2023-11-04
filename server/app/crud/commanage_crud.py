from typing import Any, List
from sqlalchemy.orm import Session

from app.schemas.commange_schema import ComManageGet, ComManage, ComManageUpdate, ComManageDelete
from app.models import commanage_model as model


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

    def create(self, commanage: ComManage) -> model.ComManage:
        """
        ComManage 객체 생성
        :param commanage: 추가하려는 ComManage 객체
        :return: model.ComManage
        """
        insert_data = model.ComManage(**dict(commanage))
        self.session.add(insert_data)
        self.session.commit()
        self.session.refresh(insert_data)
        return insert_data

    def get(self, host_id: int) -> model.ComManage:
        """
        ComManage 객체를 가져오기
        :param host_id: Host ID 값
        :return: model.ComManage
        """
        return (self.session
                .query(model.ComManage)
                .filter(model.ComManage.host_id == host_id)
                .first())

    def get_all(self, user_id: str) -> List[model.ComManage]:
        """
        User ID에 해당하는 모든 ComManage 객체를 가져오기
        :param user_id: User ID 값
        :return: List[model.ComManage]
        """
        return (self.session
                .query(model.ComManage)
                .filter(model.ComManage.user_id == user_id)
                .all())

    def update(self, origin: model.ComManage, update: ComManageUpdate) -> model.ComManage:
        """
        ComManage 객체 수정
        :param origin: 원본 데이터
        :param update: 수정하려는 데이터
        :return: model.ComManage
        """
        update_data = dict(update)
        for key, value in update_data.items():
            setattr(origin, key, value)

        self.session.add(origin)
        self.session.commit()
        self.session.refresh(origin)
        return origin

    def delete(self, host_id: int) -> model.ComManage:
        """
        ComManage 삭제
        :param host_id: 삭제하려는 Host ID 값
        :return: model.ComManage
        """
        commanage = self.get(host_id=host_id)
        commanage.deleted = True

        self.session.add(commanage)
        self.session.commit()
        self.session.refresh(commanage)
        return commanage

    def delete_all(self, user_id: str) -> None:
        """
        User ID에 해당하는 모든 ComManage 삭제 처리
        :param user_id: 삭제하려는 User ID 값
        :return: 없음
        """
        host_list = self.get_all(user_id=user_id)

        if not host_list:
            return

        for host in host_list:
            host.deleted = True
            self.session.add(host)

        self.session.commit()
