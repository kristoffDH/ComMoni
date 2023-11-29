from fastapi import status

from app.tests.api.conftest import test_client
from app.models import user_model as model
from app.schemas.user_schema import UserResponse, UserStatus

from app.crud.return_code import ReturnCode
from app.exception.crud_exception import CrudException


class TestUserAPI:
    api_path = "/api/v1/user"
    user_id = "test_user"
    user_pw = "1234567890"
    user_name = "tester"

    create_data = {
        "user_id": user_id,
        "user_pw": user_pw,
        "user_name": user_name
    }

    update_data = {
        "user_id": user_id,
        "user_pw": user_pw,
        "user_name": user_name
    }

    user_model = model.User(user_id=user_id, user_name=user_name)
    user_response_schema = UserResponse(user_id=user_id, user_name=user_name)
    user_status_schema = UserStatus(user_id=user_id, user_name=user_name, deleted=False)

    def test_create_success(self, test_client, mocker):
        """
        유저 생성 테스트
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=None)
        mocker.patch('app.crud.user_crud.UserCRUD.create', return_value=self.user_model)

        response = test_client.post(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_201_CREATED

        result = response.json()
        assert result.get("user_id") == self.user_id
        assert result.get("user_name") == self.user_name

    def test_create_fail_1(self, test_client, mocker):
        """
        유저 생성 테스트 실패. DB get error 발생
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
        유저 생성 테스트 실패. 이미 유저가 있는 경우
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=self.user_model)

        response = test_client.post(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_create_fail_3(self, test_client, mocker):
        """
        유저 생성 테스트 실패. DB create error 발생
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=None)
        mocker.patch('app.crud.user_crud.UserCRUD.create', return_value=self.user_model) \
            .side_effect = CrudException(return_code=ReturnCode.DB_CREATE_ERROR)

        response = test_client.post(
            self.api_path,
            json=self.create_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_success(self, test_client, mocker):
        """
        유저 정보 가져오기 성공
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=self.user_response_schema)

        response = test_client.get(
            self.api_path,
            params={"user_id": self.user_id}
        )

        assert response.status_code == status.HTTP_200_OK

        user_data = response.json()
        assert user_data.get("user_id") == self.user_id
        assert user_data.get("user_name") == self.user_name

    def test_get_fail_1(self, test_client, mocker):
        """
        유저 정보 가져오기 실패, DB get error 발생
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.get(
            self.api_path,
            params={"user_id": self.user_id}
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_fail_2(self, test_client, mocker):
        """
        유저 정보 가져오기 실패, 유저가 없는 경우
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=None)

        response = test_client.get(
            self.api_path,
            params={"user_id": self.user_id}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_status_success(self, test_client, mocker):
        """
        유저 상태 정보 가져오기 성공
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=self.user_status_schema)

        response = test_client.get(self.api_path + f"/{self.user_id}/status")

        assert response.status_code == status.HTTP_200_OK

        user_data = response.json()
        assert user_data.get("user_id") == self.user_id
        assert user_data.get("user_name") == self.user_name
        assert user_data.get("deleted") is False

    def test_get_status_fail_1(self, test_client, mocker):
        """
        유저 상태 정보 가져오기 실패, DB get error 발생
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get',
                     return_value=self.user_response_schema) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.get(self.api_path + f"/{self.user_id}/status")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_get_status_fail_2(self, test_client, mocker):
        """
        유저 상태 정보 가져오기 실패, 유저가 없는 경우
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=None)

        response = test_client.get(self.api_path + f"/{self.user_id}/status")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_success(self, test_client, mocker):
        """
        유저 정보 업데이트 성공
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=self.user_response_schema)
        mocker.patch('app.crud.user_crud.UserCRUD.update', return_value=ReturnCode.DB_OK)

        response = test_client.put(
            self.api_path,
            json=self.update_data
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get("message") == "update success"

    def test_update_fail_1(self, test_client, mocker):
        """
        유저 정보 업데이트 실패, DB get error 발생
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.put(
            self.api_path,
            json=self.update_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_update_fail_2(self, test_client, mocker):
        """
        유저 정보 업데이트 실패, 유저가 없는 경우
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=None)

        response = test_client.put(
            self.api_path,
            json=self.update_data
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_fail_3(self, test_client, mocker):
        """
        유저 정보 업데이트 실패, DB update error 발생
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=self.user_response_schema)
        mocker.patch('app.crud.user_crud.UserCRUD.update', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_UPDATE_ERROR)

        response = test_client.put(
            self.api_path,
            json=self.update_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_update_fail_4(self, test_client, mocker):
        """
        유저 정보 업데이트 실패, DB update None 발생
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=self.user_response_schema)
        mocker.patch('app.crud.user_crud.UserCRUD.update', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_UPDATE_NONE)

        response = test_client.put(
            self.api_path,
            json=self.update_data
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_delete_success(self, test_client, mocker):
        """
        유저 삭제 성공, 유저에 연관된 commanage 데이터 전부 삭제 처리
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=self.user_response_schema)
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.delete_all',
                     return_value=ReturnCode.DB_OK)
        mocker.patch('app.crud.user_crud.UserCRUD.delete', return_value=ReturnCode.DB_OK)

        response = test_client.delete(
            self.api_path + f"/{self.user_id}"
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data.get("message") == "update success"

    def test_delete_fail_1(self, test_client, mocker):
        """
        유저 삭제 실패, 유저 get DB error 발생
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=None) \
            .side_effect = CrudException(return_code=ReturnCode.DB_GET_ERROR)

        response = test_client.delete(
            self.api_path + f"/{self.user_id}"
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_delete_fail_2(self, test_client, mocker):
        """
        유저 삭제 실패, 유저가 없는 경우
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=None)

        response = test_client.delete(
            self.api_path + f"/{self.user_id}"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_fail_3(self, test_client, mocker):
        """
        유저 삭제 실패, 유저에 연관된 commanage 삭제 실패
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=self.user_response_schema)
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.delete_all',
                     return_value=ReturnCode.DB_OK) \
            .side_effect = CrudException(return_code=ReturnCode.DB_ALL_DELETE_ERROR)

        response = test_client.delete(
            self.api_path + f"/{self.user_id}"
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_delete_fail_4(self, test_client, mocker):
        """
        유저 삭제 실패, 유저 DB delete error
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=self.user_response_schema)
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.delete_all',
                     return_value=ReturnCode.DB_OK)
        mocker.patch('app.crud.user_crud.UserCRUD.delete', return_value=ReturnCode.DB_OK) \
            .side_effect = CrudException(return_code=ReturnCode.DB_DELETE_ERROR)

        response = test_client.delete(
            self.api_path + f"/{self.user_id}"
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_delete_fail_5(self, test_client, mocker):
        """
        유저 삭제 실패, User Delete None 발생
        """
        mocker.patch('app.crud.user_crud.UserCRUD.get', return_value=self.user_response_schema)
        mocker.patch('app.crud.commanage_crud.CommanageCRUD.delete_all',
                     return_value=ReturnCode.DB_OK)
        mocker.patch('app.crud.user_crud.UserCRUD.delete', return_value=ReturnCode.DB_OK) \
            .side_effect = CrudException(return_code=ReturnCode.DB_DELETE_NONE)

        response = test_client.delete(
            self.api_path + f"/{self.user_id}"
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
