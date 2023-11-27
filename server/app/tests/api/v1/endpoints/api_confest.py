import pytest

from app.models.user_model import User
from app.models.commanage_model import ComManage
from app.tests.api.conftest import session

user_id = "test_user"
user_pw = "1234567890"
user_name = "tester"


@pytest.fixture(scope="module")
def create_user(session):
    """
    테스트용 User 생성
    """
    user = User(
        user_id=user_id,
        user_pw=user_pw,
        user_name=user_name,
    )

    session.add(user)
    session.commit()


host_name = "test_host1"
host_name_2 = "test_host2"
host_ip = "127.0.0.1"
host_memory = "12G"
host_disk = "256G"


@pytest.fixture(scope="module")
def create_commanage(session):
    """
    테스트용 Commanage 생성
    """
    commanage = ComManage(
        user_id=user_id,
        host_name=host_name,
        host_ip=host_ip,
        memory=host_memory,
        disk=host_disk
    )

    session.add(commanage)
    session.commit()
