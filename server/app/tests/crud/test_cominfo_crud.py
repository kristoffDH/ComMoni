from unittest import mock
from datetime import datetime

from mock_alchemy.mocking import AlchemyMagicMock, UnifiedAlchemyMagicMock
from sqlalchemy.exc import SQLAlchemyError

from app.models import cominfo_model as model
from app.schemas.cominfo_schema import ComInfoGet, ComInfoCreate, ComInfoRT
from app.crud.cominfo_crud import CominfoCRUD, CominfoRtCRUD

from app.crud.return_code import ReturnCode


class TestCominfoCRUD:
    def test_create_success(self):
        """데이터 생성 성공"""
        session = AlchemyMagicMock()

        make_datetime = str(datetime.now())
        create_cominfo_data = ComInfoCreate(host_id=1, make_datetime=make_datetime)
        assert CominfoCRUD(session).create(create_cominfo_data) == ReturnCode.DB_OK

    def test_create_fail_by_db_error(self):
        """데이터 생성 실패(DB 에러 발생)"""
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        make_datetime = str(datetime.now())
        create_cominfo_data = ComInfoCreate(host_id=1, make_datetime=make_datetime)
        assert CominfoCRUD(session).create(create_cominfo_data) == ReturnCode.DB_CREATE_ERROR


class TestCominfoRtCRUD:
    def test_create_success(self):
        """데이터 생성 성공"""
        host_id = 1
        session = AlchemyMagicMock()

        create_cominfort_data = ComInfoRT(host_id=host_id)
        assert CominfoRtCRUD(session).create(create_cominfort_data) == ReturnCode.DB_OK

    def test_create_fail_by_db_error(self):
        """데이터 생성 실패(DB 에러 발생)"""
        host_id = 1
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        create_cominfort_data = ComInfoRT(host_id=host_id)
        assert CominfoRtCRUD(session).create(create_cominfort_data) == ReturnCode.DB_CREATE_ERROR

    def test_update_success(self):
        """데이터 수정 성공"""
        host_id = 1
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 1

        update_data = ComInfoRT(host_id=host_id)
        assert CominfoRtCRUD(session).update(update_data=update_data) == ReturnCode.DB_OK

    def test_update_none(self):
        """수정된 데이터가 없는 경우"""
        host_id = 1
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 0

        update_data = ComInfoRT(host_id=host_id)
        assert CominfoRtCRUD(session).update(update_data=update_data) == ReturnCode.DB_UPDATE_NONE

    def test_update_fail_by_db_error(self):
        """데이터 수정 실패 (DB 에러 발생)"""
        host_id = 1
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        update_data = ComInfoRT(host_id=host_id)
        assert CominfoRtCRUD(session).update(update_data=update_data) == ReturnCode.DB_UPDATE_ERROR
