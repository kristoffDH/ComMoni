from typing import Any
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserUpdate
from app.models import user_model as model
from app.core.dictionary_util import dictionary_util


class UserCRUD:
    """
    User Model에 대한 CURD 구현 클래스
    """

    def __init__(self, session: Session):
        """
        생성자
        :param session: DB Session 객체
        """
        self.session = session

    def create(self, user: UserCreate) -> model.User:
        """
        User 객체 생성
        :param user: 추가하려는 User 객체
        :return: model.User
        """
        insert_data = model.User(**dict(user))
        self.session.add(insert_data)
        self.session.commit()
        self.session.refresh(insert_data)
        return insert_data

    def get(self, user_id: str) -> model.User:
        """
        User 객체를 가져오기
        :param user_id: User ID 값
        :return: model.User
        """
        return (self.session
                .query(model.User)
                .filter(model.User.user_id == user_id)
                .first())

    def update(self, update_data: UserUpdate) -> None:
        """
        User 객체 수정
        :param update_data: 수정하려는 데이터
        :return: model.User
        """
        # 값이 None인 키 삭제
        filtered_dict = dictionary_util.remove_none(dict(update_data))

        (self.session.query(model.User)
         .filter(model.User.user_id == update_data.user_id)
         .update(filtered_dict)
         )
        self.session.commit()

    def delete(self, user_id: str) -> None:
        """
        User 삭제
        :param user_id: 삭제하려는 User ID
        :return:
        """

        (self.session.query(model.User)
         .filter(model.User.user_id == user_id)
         .update({"deleted": True})
         )
        self.session.commit()
