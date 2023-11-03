from typing import Any
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, User, UserUpdate
from app.models import user_model as model


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

    def update(self, origin: User, update: UserUpdate) -> model.User:
        """
        User 객체 수정
        :param origin: 원본 데이터
        :param update: 수정하려는 데이터
        :return: model.User
        """
        update_data = dict(update)
        for key, value in update_data.items():
            setattr(origin, key, value)

        self.session.add(origin)
        self.session.commit()
        self.session.refresh(origin)
        return origin
