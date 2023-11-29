from fastapi import status

from app.tests.api.conftest import test_client
from app.models.user_model import User
from app.models import commanage_model as model
from app.schemas.commange_schema import ComManageResponse

from app.core.return_code import ReturnCode
from app.exception.crud_exception import CrudException


class TestCommanageAPI:
    api_path = "/api/v1/commanage"
    user_id = "test_user"
    host_id = 1
    host_name = "tester"
    host_ip = "127.0.0.1"
    memory = "32G"
    disk = "512G"
    deleted = False
    user_name = "tester"

    create_data = {
        "user_id": user_id,
        "host_id": host_id,
        "host_name": host_name,
        "host_ip": host_ip,
        "memory": memory,
        "disk": disk,
        "deleted": deleted
    }

    update_data = {
        "user_id": user_id,
        "host_id": host_id,
        "host_name": host_name,
        "host_ip": host_ip,
        "memory": memory,
        "disk": disk,
        "deleted": deleted
    }

    user_model = User(user_id=user_id, user_name=user_name)
    commanage_model = model.ComManage(
        user_id=user_id,
        host_id=host_id,
        host_name=host_name,
        host_ip=host_ip,
        memory=memory,
        disk=disk,
        deleted=deleted
    )
    commanage_response_schema = ComManageResponse(host_id=host_id)

    def test_create_success(self, test_client, mocker):
        """
        Commaange 생성 테스트 성공
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=self.user_model)
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.create', return_value=self.commanage_response_schema)

        response = test_client.post(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_201_CREATED

        result = response.json()
        assert result.get("host_id") == self.host_id

    def test_create_fail_1(self, test_client, mocker):
        """
        Commanage 생성 테스트 실패. User DB get error 발생
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.post(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_create_fail_2(self, test_client, mocker):
        """
        Commanage 생성 테스트 실패. User 가 없는 경우
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=None)

        response = test_client.post(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_fail_3(self, test_client, mocker):
        """
        Commaange 생성 실패, DB create error 발생
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=self.user_model)
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.create', return_value=None) \
            .side_effect = CrudException(ReturnCode.DB_CREATE_ERROR)

        response = test_client.post(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_success(self, test_client, mocker):
        """
          host_id로 Commaange 가져오기 성공
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=self.commanage_model)

        response = test_client.get(self.api_path + f"/{self.host_id}")

        assert response.status_code == status.HTTP_200_OK

        result = response.json()
        assert result.get("user_id") == self.user_id
        assert result.get("host_id") == self.host_id
        assert result.get("host_name") == self.host_name
        assert result.get("host_ip") == self.host_ip
        assert result.get("memory") == self.memory
        assert result.get("disk") == self.disk
        assert result.get("deleted") == self.deleted

    def test_get_fail(self, test_client, mocker):
        """
          host_id로 Commaange 가져오기 실패
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.get(self.api_path + f"/{self.host_id}")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_all_success(self, test_client, mocker):
        """
          user_id로 Commaange 가져오기 성공
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get_all', return_value=[self.commanage_model])

        response = test_client.get(self.api_path + f"/all/{self.user_id}")

        assert response.status_code == status.HTTP_200_OK

        result = response.json()
        assert result[0].get("user_id") == self.user_id
        assert result[0].get("host_id") == self.host_id
        assert result[0].get("host_name") == self.host_name
        assert result[0].get("host_ip") == self.host_ip
        assert result[0].get("memory") == self.memory
        assert result[0].get("disk") == self.disk
        assert result[0].get("deleted") == self.deleted

    def test_get_all_fail(self, test_client, mocker):
        """
        user_id로 Commaange 가져오기 실패
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get_all', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.get(self.api_path + f"/all/{self.user_id}")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_update_success(self, test_client, mocker):
        """
        Commanage 정보 업데이트 성공
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=self.commanage_model)
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.update', return_value=ReturnCode.DB_OK)

        response = test_client.put(
            self.api_path,
            json=self.update_data
        )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data.get("message") == "update success"

    def test_update_fail_1(self, test_client, mocker):
        """
        Commanage 정보 업데이트 실패, DB get error 발생
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.put(
            self.api_path,
            json=self.update_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_update_fail_2(self, test_client, mocker):
        """
        Commanage 정보 업데이트 실패, Commanage가 없는 경우
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=None)

        response = test_client.put(
            self.api_path,
            json=self.update_data
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_fail_3(self, test_client, mocker):
        """
        Commanage 정보 업데이트 실패, DB update error 발생
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=self.commanage_model)
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.update', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_UPDATE_ERROR)

        response = test_client.put(
            self.api_path,
            json=self.update_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_update_fail_4(self, test_client, mocker):
        """
        Commanage 정보 업데이트 실패, DB update none 발생
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=self.commanage_model)
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.update', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_UPDATE_NONE)

        response = test_client.put(
            self.api_path,
            json=self.update_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_delete_success(self, test_client, mocker):
        """
        Commanage 정보 삭제 성공
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=self.host_id)
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.delete', return_value=ReturnCode.DB_OK)

        response = test_client.delete(
            self.api_path + f"/{self.host_id}"
        )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data.get("message") == "delete success"

    def test_delete_fail_1(self, test_client, mocker):
        """
        Commanage 정보 삭제 실패, DB get error 발생
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.delete(
            self.api_path + f"/{self.host_id}"
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_delete_fail_2(self, test_client, mocker):
        """
        Commanage 정보 삭제 실패, Commanage가 없는 경우
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=None)

        response = test_client.delete(
            self.api_path + f"/{self.host_id}"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_fail_3(self, test_client, mocker):
        """
        Commanage 정보 삭제 실패, DB delete error 발생
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=self.host_id)
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.delete', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_DELETE_ERROR)

        response = test_client.delete(
            self.api_path + f"/{self.host_id}"
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_delete_fail_4(self, test_client, mocker):
        """
        Commanage 정보 삭제 실패, DB delete None 발생
        """
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.get', return_value=self.host_id)
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.delete', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_DELETE_NONE)

        response = test_client.delete(
            self.api_path + f"/{self.host_id}"
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
