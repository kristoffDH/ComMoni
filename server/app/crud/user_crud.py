from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.user_schema import UserGet, UserCreate, UserVerify
from app.models import user_model as model
from app.core.dictionary_util import dictionary_util

from passlib.context import CryptContext

from app.core.return_code import ReturnCode
from app.exception.crud_exception import CrudException

from app.core.log import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    비밀번호 해시값 비교 인증
    :param plain_password: 평문 비밀번호
    :param hashed_password: 해시된 비밀번호
    :return: bool
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    비밀번호 해시하여 반환
    :param password: 원본 비밀번호
    :return: 해시된 비밀번호
    """
    return pwd_context.hash(password)


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

        try:
            self.session.add(insert_data)
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[User]DB Err : {err}")
            self.session.rollback()
            raise CrudException(return_code=ReturnCode.DB_CREATE_ERROR)

        return insert_data

    def get(self, user: UserGet) -> model.User:
        """
        User 객체를 가져오기
        :param user: user 요청 객체
        :return: model.User
        """
        try:
            return self.session \
                .query(model.User) \
                .filter(model.User.user_id == user.user_id) \
                .first()
        except SQLAlchemyError as err:
            logger.error(f"[User]DB Err : {err}")
            raise CrudException(return_code=ReturnCode.DB_GET_ERROR)

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
            raise CrudException(return_code=ReturnCode.DB_UPDATE_ERROR)

        if updated == 0:
            logger.error("[User]Update is None")
            raise CrudException(return_code=ReturnCode.DB_UPDATE_NONE)

        return ReturnCode.DB_OK

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
            raise CrudException(return_code=ReturnCode.DB_DELETE_ERROR)

        if deleted == 0:
            logger.error("[User]Delete is None")
            raise CrudException(return_code=ReturnCode.DB_DELETE_NONE)

        return ReturnCode.DB_OK

    def authenticate_user(self, user: UserVerify) -> model.User:
        """
        유저 인증 확인
        :param user: 인증하려는 유저 정보
        :return: model.User
        """
        try:
            get_user = self.session \
                .query(model.User) \
                .filter(model.User.user_id == user.user_id) \
                .first()
        except SQLAlchemyError as err:
            logger.error(f"[User]DB Err : {err}")
            raise CrudException(return_code=ReturnCode.DB_GET_ERROR)

        if not get_user:
            raise CrudException(return_code=ReturnCode.USER_NOT_FOUND)

        if not verify_password(plain_password=user.user_pw,
                               hashed_password=get_user.user_pw):
            raise CrudException(return_code=ReturnCode.USER_PW_INVALID)

        if get_user.deleted:
            raise CrudException(return_code=ReturnCode.USER_IS_DELETED)

        return get_user
