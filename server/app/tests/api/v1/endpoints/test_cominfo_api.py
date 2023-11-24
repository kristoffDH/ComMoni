from fastapi import status
from datetime import datetime

from app.tests.api.conftest import test_client
from app.models.commanage_model import ComManage
from app.models import cominfo_model as model
from app.schemas.cominfo_schema import ComInfo, ComInfoRT, ComInfoGet

from app.crud.return_code import ReturnCode
from app.exception.crud_exception import CrudException


class TestCominfoAPI:
    api_path = "/api/v1/cominfo"

    host_id = 1
    cpu_utilization = 10.1
    memory_utilization = 20.2
    disk_utilization = 30.3
    make_datetime = str(datetime.now())

    start_dt = str(datetime.now())
    end_et = str(datetime.now())
    skip = 5
    limit = 100

    create_data = {
        "host_id": host_id,
        "cpu_utilization": cpu_utilization,
        "memory_utilization": memory_utilization,
        "disk_utilization": disk_utilization,
        "make_datetime": make_datetime
    }

    commanage_model = ComManage(host_id=host_id)
    cominfo_get_schema = ComInfoGet(host_id=host_id)
    cominfo_schema = [ComInfo(
        host_id=host_id,
        cpu_utilization=cpu_utilization,
        memory_utilization=memory_utilization,
        disk_utilization=disk_utilization,
        make_datetime=str(datetime.now())
    )]

    def test_create_success(self, test_client, mocker):
        """
        Cominfo 생성 테스트 성공
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=self.commanage_model)
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.create', return_value=self.cominfo_get_schema)

        response = test_client.post(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_201_CREATED

        result = response.json()
        assert result.get("host_id") == self.host_id

    def test_create_fail_1(self, test_client, mocker):
        """
        Cominfo 생성 테스트 실패, DB get error 발생
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.post(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_create_fail_2(self, test_client, mocker):
        """
        Cominfo 생성 테스트 실패, Commanage 없는 경우
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=None)

        response = test_client.post(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_fail_3(self, test_client, mocker):
        """
        Cominfo 생성 테스트 실패, DB create error 발생
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=self.commanage_model)
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.create', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_CREATE_ERROR)

        response = test_client.post(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_success_1(self, test_client, mocker):
        """
        Cominfo 가져오기 성공, 시작 날짜만 있는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_by_datetime', return_value=self.cominfo_schema)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"start_dt": self.start_dt}
        )

        assert response.status_code == status.HTTP_200_OK

    def test_get_success_2(self, test_client, mocker):
        """
        Cominfo 가져오기 성공, 종료 날짜만 있는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_by_datetime', return_value=self.cominfo_schema)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"end_dt": self.end_et}
        )

        assert response.status_code == status.HTTP_200_OK

    def test_get_success_3(self, test_client, mocker):
        """
        Cominfo 가져오기 성공, 시작, 종료 날짜 있는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_by_datetime', return_value=self.cominfo_schema)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"start_dt": self.start_dt, "end_dt": self.end_et}
        )

        assert response.status_code == status.HTTP_200_OK

    def test_get_success_4(self, test_client, mocker):
        """
        Cominfo 가져오기 skip 있는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_multiline', return_value=self.cominfo_schema)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"skip": self.skip}
        )

        assert response.status_code == status.HTTP_200_OK

    def test_get_success_5(self, test_client, mocker):
        """
        Cominfo 가져오기 limit 있는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_multiline', return_value=self.cominfo_schema)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"limit": self.limit}
        )

        assert response.status_code == status.HTTP_200_OK

    def test_get_success_6(self, test_client, mocker):
        """
        Cominfo 가져오기 성공, skip, limit 있는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_multiline', return_value=self.cominfo_schema)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"skip": self.skip, "limit": self.limit}
        )

        assert response.status_code == status.HTTP_200_OK

    def test_get_fail_1(self, test_client, mocker):
        """
        Cominfo 가져오기 실패, 시작 날짜만 있는 경우, DB get error 발생
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_by_datetime', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"start_dt": self.start_dt}
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_fail_2(self, test_client, mocker):
        """
        Cominfo 가져오기 실패, 종료 날짜만 있는 경우, DB get error 발생
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_by_datetime', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"end_dt": self.end_et}
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_fail_3(self, test_client, mocker):
        """
        Cominfo 가져오기 실패, 시작, 종료 날짜 있는 경우, DB get error 발생
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_by_datetime', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"start_dt": self.start_dt, "end_dt": self.end_et}
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_fail_4(self, test_client, mocker):
        """
        Cominfo 가져오기 실패, 시작 날짜만 있는 경우, 데이터가 없는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_by_datetime', return_value=None)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"start_dt": self.start_dt}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_fail_5(self, test_client, mocker):
        """
        Cominfo 가져오기 실패, 종료 날짜만 있는 경우, 데이터가 없는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_by_datetime', return_value=None)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"end_dt": self.end_et}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_fail_6(self, test_client, mocker):
        """
        Cominfo 가져오기 실패, 시작, 종료 날짜 있는 경우, 데이터가 없는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_by_datetime', return_value=None)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"start_dt": self.start_dt, "end_dt": self.end_et}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_fail_7(self, test_client, mocker):
        """
        Cominfo 가져오기 실패, skip 있는 경우, DB get error 발생
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_multiline', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"skip": self.skip}
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_fail_8(self, test_client, mocker):
        """
        Cominfo 가져오기 실패, limit 있는 경우, DB get error 발생
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_multiline', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"limit": self.limit}
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_fail_9(self, test_client, mocker):
        """
        Cominfo 가져오기 실패, skip, limit 있는 경우, DB get error 발생
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_multiline', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"skip": self.skip, "limit": self.limit}
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_fail_10(self, test_client, mocker):
        """
        Cominfo 가져오기 실패, skip 있는 경우, 데이터가 없는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_multiline', return_value=None)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"skip": self.skip}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_fail_11(self, test_client, mocker):
        """
        Cominfo 가져오기 실패, limit 있는 경우, 데이터가 없는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_multiline', return_value=None)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"limit": self.limit}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_fail_12(self, test_client, mocker):
        """
        Cominfo 가져오기 실패, skip, limit 있는 경우, 데이터가 없는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoCRUD.get_multiline', return_value=None)

        response = test_client.get(
            self.api_path + f"/{self.host_id}",
            params={"skip": self.skip, "limit": self.limit}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCominfoRtAPI:
    api_path = "/api/v1/cominfo/realtime"

    host_id = 1
    cpu_utilization = 10.1
    memory_utilization = 20.2
    disk_utilization = 30.3
    make_datetime = str(datetime.now())

    model_coinfo_rt = model.ComInfoRT(
        host_id=host_id,
        cpu_utilization=cpu_utilization,
        memory_utilization=memory_utilization,
        disk_utilization=disk_utilization,
    )
    create_data = {
        "host_id": host_id,
        "cpu_utilization": cpu_utilization,
        "memory_utilization": memory_utilization,
        "disk_utilization": disk_utilization,
    }

    def test_put_succces_1(self, test_client, mocker):
        """
        comfinort put 테스트 성공 (생성)
        """
        mocker.patch('app.crud.cominfo_crud.CominfoRtCRUD.get', return_value=None)
        mocker.patch('app.crud.cominfo_crud.CominfoRtCRUD.create', return_value=self.model_coinfo_rt)

        response = test_client.put(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result.get("message") == f"host[{self.host_id}] create success"

    def test_put_succces_2(self, test_client, mocker):
        """
        comfinort put 테스트 성공 (업데이트)
        """
        mocker.patch('app.crud.cominfo_crud.CominfoRtCRUD.get', return_value=self.model_coinfo_rt)
        mocker.patch('app.crud.cominfo_crud.CominfoRtCRUD.update', return_value=self.model_coinfo_rt)

        response = test_client.put(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result.get("message") == f"update success"

    def test_put_fail_1(self, test_client, mocker):
        """
        comfinort put 테스트 실패 (생성), DB get error 발생
        """
        mocker.patch('app.crud.cominfo_crud.CominfoRtCRUD.get', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.put(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_put_fail_2(self, test_client, mocker):
        """
        comfinort put 테스트 실패 (생성), DB get error 발생
        """
        mocker.patch('app.crud.cominfo_crud.CominfoRtCRUD.get', return_value=None)
        mocker.patch('app.crud.cominfo_crud.CominfoRtCRUD.create', return_value=self.model_coinfo_rt) \
            .side_effect = CrudException(return_code=ReturnCode.DB_CREATE_ERROR)

        response = test_client.put(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_put_fail_3(self, test_client, mocker):
        """
        comfinort put 테스트 실패 (수정), DB get error 발생
        """
        mocker.patch('app.crud.cominfo_crud.CominfoRtCRUD.get', return_value=None)
        mocker.patch('app.crud.cominfo_crud.CominfoRtCRUD.update', return_value=self.model_coinfo_rt) \
            .side_effect = CrudException(return_code=ReturnCode.DB_UPDATE_ERROR)

        response = test_client.put(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_success(self, test_client, mocker):
        """
        cominfort 가져오기 성공
        """
        mocker.patch('app.crud.cominfo_crud.CominfoRtCRUD.get', return_value=self.model_coinfo_rt)

        response = test_client.get(
            self.api_path + f"/{self.host_id}"
        )

        assert response.status_code == status.HTTP_200_OK
        result = response.json()

        assert result.get("host_id") == self.host_id
        assert result.get("cpu_utilization") == self.cpu_utilization
        assert result.get("memory_utilization") == self.memory_utilization
        assert result.get("disk_utilization") == self.disk_utilization

    def test_get_fail_1(self, test_client, mocker):
        """
        cominfort 가져오기 실패, DB get error 발생
        """
        mocker.patch('app.crud.cominfo_crud.CominfoRtCRUD.get', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_CREATE_ERROR)

        response = test_client.get(
            self.api_path + f"/{self.host_id}"
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_fail_2(self, test_client, mocker):
        """
        cominfort 가져오기 실패, 데이터가 없는 경우
        """
        mocker.patch('app.crud.cominfo_crud.CominfoRtCRUD.get', return_value=None)

        response = test_client.get(
            self.api_path + f"/{self.host_id}"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
