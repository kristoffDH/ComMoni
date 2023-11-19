from unittest import mock

from mock_alchemy.mocking import AlchemyMagicMock, UnifiedAlchemyMagicMock
from sqlalchemy.exc import SQLAlchemyError

from app.models import user_model as model
from app.schemas.user_schema import UserCreate, UserGet
from app.crud.user_crud import UserCRUD

from app.crud.return_code import ReturnCode


class TestUserCRUD:

    def test_create_success(self):
        """데이터 생성 성공"""
        create_user_data = UserCreate(user_id="test_user", user_pw="1234567890")
        session = AlchemyMagicMock()

        assert UserCRUD(session).create(create_user_data) == ReturnCode.DB_OK

    def test_create_fail_by_db_error(self):
        """데이터 생성 실패(DB 에러 발생)"""
        session = AlchemyMagicMock()

        # commit에서 예외 발생하도록 설정
        session.commit.side_effect = SQLAlchemyError()

        create_user_data = UserCreate(user_id="test_user", user_pw="1234567890")
        assert UserCRUD(session).create(create_user_data) == ReturnCode.DB_CREATE_ERROR

    def test_update_success(self):
        """데이터 수정 성공"""
        user_id = "test_user"
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 1

        update_data = UserGet(user_id=user_id)
        assert UserCRUD(session).update(update_data=update_data) == ReturnCode.DB_OK

    def test_update_none(self):
        """수정된 데이터가 없는 경우"""
        user_id = "test_user"
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 0

        update_data = UserGet(user_id=user_id)
        assert UserCRUD(session).update(update_data=update_data) == ReturnCode.DB_UPDATE_NONE

    def test_update_fail_by_db_error(self):
        """데이터 수정 실패 (DB 에러 발생)"""
        user_id = "test_user"
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        update_data = UserGet(user_id=user_id)
        assert UserCRUD(session).update(update_data=update_data) == ReturnCode.DB_UPDATE_ERROR

    def test_delete_success(self):
        """데이터 삭제 성공"""
        user_id = "test_user"
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 1

        delete_data = UserGet(user_id=user_id)
        assert UserCRUD(session).delete(user=delete_data) == ReturnCode.DB_OK

    def test_delete_none(self):
        """삭제된 데이터가 없는 경우"""
        user_id = "test_user"
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 0

        delete_data = UserGet(user_id=user_id)
        assert UserCRUD(session).delete(user=delete_data) == ReturnCode.DB_DELETE_NONE

    def test_delete_fail_by_db_error(self):
        """데이터 삭제 실패 (DB 에러 발생)"""
        user_id = "test_user"
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        delete_data = UserGet(user_id=user_id)
        assert UserCRUD(session).delete(user=delete_data) == ReturnCode.DB_DELETE_ERROR

    def test_get(self):
        """데이터 가져오기"""
        user_id = "test_user"
        user_pw = "1234567890"
        user_name = "tester"
        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(model.User),
              mock.call.filter(model.User.user_id == user_id)],
             [model.User(user_id=user_id, user_pw=user_pw, user_name=user_name, deleted=False)])
        ])

        requset_user_get = UserGet(user_id=user_id)
        result = UserCRUD(session).get(requset_user_get)

        assert result.user_id == user_id
        assert result.user_pw == user_pw
        assert result.user_name == user_name
        assert result.deleted is False
