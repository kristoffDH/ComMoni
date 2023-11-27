from unittest import mock

from mock_alchemy.mocking import AlchemyMagicMock, UnifiedAlchemyMagicMock
from sqlalchemy.exc import SQLAlchemyError

from app.models import commanage_model as model
from app.schemas.commange_schema import ComManage, ComManageByUser, ComManageByHost
from app.crud.commanage_crud import CommanageCRUD

from app.crud.return_code import ReturnCode


class TestCommanageCRUD:
    def test_create_success(self):
        """데이터 생성 성공"""
        session = AlchemyMagicMock()

        create_commanage_data = ComManageByUser(user_id="test_user", host_id=1)
        result, host_id = CommanageCRUD(session).create(create_commanage_data)
        assert result == ReturnCode.DB_OK
        assert host_id == 1

    def test_create_fail_by_db_error(self):
        """데이터 생성 실패(DB 에러 발생)"""
        session = AlchemyMagicMock()

        # commit에서 예외 발생하도록 설정
        session.commit.side_effect = SQLAlchemyError()

        create_commanage_data = ComManageByUser(user_id="test_userh")
        result, _ = CommanageCRUD(session).create(create_commanage_data)
        assert result == ReturnCode.DB_CREATE_ERROR

    def test_update_success(self):
        """데이터 수정 성공"""
        host_id = 1
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 1

        update_data = ComManageByHost(host_id=host_id)
        assert CommanageCRUD(session).update(update_data=update_data) == ReturnCode.DB_OK

    def test_update_none(self):
        """수정된 데이터가 없는 경우"""
        host_id = 1
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 0

        update_data = ComManageByHost(host_id=host_id)
        assert CommanageCRUD(session).update(update_data=update_data) == ReturnCode.DB_UPDATE_NONE

    def test_update_fail_by_db_error(self):
        """데이터 수정 실패 (DB 에러 발생)"""
        host_id = 1
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        update_data = ComManageByHost(host_id=host_id)
        assert CommanageCRUD(session).update(update_data=update_data) == ReturnCode.DB_UPDATE_ERROR

    def test_delete_success(self):
        """데이터 삭제 성공"""
        host_id = 1
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 1

        delete_data = ComManageByHost(host_id=host_id)
        assert CommanageCRUD(session).delete(delete_data=delete_data) == ReturnCode.DB_OK

    def test_delete_none(self):
        """삭제된 데이터가 없는 경우"""
        host_id = 1
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 0

        delete_data = ComManageByHost(host_id=host_id)
        assert CommanageCRUD(session).delete(delete_data=delete_data) == ReturnCode.DB_DELETE_NONE

    def test_delete_fail_by_db_error(self):
        """삭제된 데이터가 없는 경우"""
        host_id = 1
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        delete_data = ComManageByHost(host_id=host_id)
        assert CommanageCRUD(session).delete(delete_data=delete_data) == ReturnCode.DB_DELETE_ERROR

    def test_get(self):
        """데이터 가져오기"""
        host_id = 1
        user_id = "test_user"
        host_name = "tester"

        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(model.ComManage),
              mock.call.filter(model.ComManage.host_id == host_id)],
             [model.ComManage(
                 host_id=host_id,
                 user_id=user_id,
                 host_name=host_name
             )])
        ])

        request_commange_data = ComManageByHost(host_id=host_id)
        result = CommanageCRUD(session).get(request_commange_data)

        assert result.host_id == host_id
        assert result.user_id == user_id
        assert result.host_name == host_name

    def test_get_all(self):
        """데이터 전체 가져오기"""
        user_id = "test_user"
        test_data = [{"user_id": "test_user", "host_id": idx, "host_name": f"test_user_{idx}"}
                     for idx in range(3)]

        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(model.ComManage),
              mock.call.filter(model.ComManage.user_id == user_id)],
             [model.ComManage(**data) for data in test_data])
        ])

        request_commange_data = ComManageByUser(user_id=user_id)
        result = CommanageCRUD(session).get_all(request_commange_data)

        assert len(result) == 3
        assert result[0].user_id == user_id
