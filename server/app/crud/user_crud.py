from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.user_schema import UserGet, UserCreate
from app.models import user_model as model
from app.core.dictionary_util import dictionary_util
from app.core.log import logger
from app.crud import return_code


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

    def create(self, user: UserCreate) -> int:
        """
        User 객체 생성
        :param user: 추가하려는 User 객체
        :return: return_code
        """
        insert_data = model.User(**dict(user))
        try:
            self.session.add(insert_data)
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[User]DB Err : {err}")
            self.session.rollback()
            return return_code.DB_CREATE_ERROR

        return return_code.DB_OK

    def get(self, user: UserGet) -> model.User:
        """
        User 객체를 가져오기
        :param user: user 요청 객체
        :return: model.User
        """
        return self.session \
            .query(model.User) \
            .filter(model.User.user_id == user.user_id) \
            .first()

    def update(self, update_data: UserGet) -> int:
        """
        User 객체 수정
        :param update_data: 수정하려는 데이터
        :return: return_code
        """
        # 값이 None인 키 삭제
        filtered_dict = dictionary_util.remove_none(dict(update_data))

        try:
            updated = self.session.query(model.User) \
                .filter(model.User.user_id == update_data.user_id) \
                .update(filtered_dict)
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[User]DB Error : {err}")
            self.session.rollback()
            return return_code.DB_UPDATE_ERROR

        return return_code.DB_OK if updated > 0 else return_code.DB_UPDATE_NONE

    def delete(self, user: UserGet) -> int:
        """
        User 삭제
        :param user: 삭제 요청 객체
        :return: return_code
        """
        try:
            deleted = self.session.query(model.User) \
                .filter(model.User.user_id == user.user_id) \
                .update({"deleted": True})
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[User]DB Err : {err}")
            self.session.rollback()
            return return_code.DB_DELETE_ERROR

        return return_code.DB_OK if deleted > 0 else return_code.DB_DELETE_NONE
