from app.tests.test_config import client, session

user_id = "test_user_1"
user_pw = "1234567890"
user_name = "test_user_name_1"
update_user_name = "test_update_name"
update_user_pw = "0000000000"


def test_user_create(client):
    """
    유저 생성 테스트
    """
    response = client.post(
        "/api/v1/user",
        json={"user_id": user_id, "user_pw": user_pw, "user_name": user_name},
    )

    assert response.status_code == 201
    assert response.json() == {"user_id": user_id, "user_name": user_name}


def test_user_create_fail(client):
    """
    유저 생성 테스트 (중복 아이디로 생성)
    """
    response = client.post(
        "/api/v1/user",
        json={"user_id": user_id, "user_pw": user_pw, "user_name": user_name},
    )
    assert response.status_code == 409
    assert response.json() == {'message': f'{user_id} is already existed.'}


def test_user_get(client):
    """
    사용자 읽기
    """
    response = client.get(f"/api/v1/user?user_id={user_id}")
    assert response.status_code == 200
    assert response.json() == {"user_id": user_id, "user_name": user_name}


def test_user_get_invalid_id(client):
    """
    존재하지 않는 사용자
    """
    invalid_user_id = "test_invalid_id"
    response = client.get(f"/api/v1/user?user_id={invalid_user_id}")
    assert response.status_code == 404
    assert response.json() == {"message": f"{invalid_user_id} is not existed."}


def test_user_get_status(client):
    """
    사용자 상태 읽기
    """
    response = client.get(f"/api/v1/user/{user_id}/status")
    assert response.status_code == 200
    assert response.json() == {"user_id": user_id, "user_name": user_name, "deleted": False}


def test_user_update(client):
    """
    사용자 수정
    """
    response = client.put(
        "/api/v1/user",
        json={"user_id": user_id, "user_pw": update_user_pw, "user_name": update_user_name},
    )
    assert response.status_code == 204

    response = client.get(f"/api/v1/user?user_id={user_id}")
    assert response.status_code == 200
    assert response.json() == {"user_id": user_id, "user_name": update_user_name}


def test_user_delete(client):
    """
    사용자 삭제, 연관된 commanage의 호스트도 전부 삭제되는지 확인
    """
    for id in range(1, 4):
        response = client.post(
            "/api/v1/commanage",
            json={"user_id": user_id},
        )

        assert response.status_code == 201
        assert response.json() == {"host_id": id}

    # client delete
    response = client.delete(
        f"/api/v1/user/{user_id}"
    )
    assert response.status_code == 204

    # deleted client check
    response = client.get(f"/api/v1/user/{user_id}/status")
    assert response.status_code == 200

    status = response.json()
    assert status["deleted"] is True

    # deleted commanage chck
    for id in range(1, 4):
        response = client.get(
            f"/api/v1/commanage?host_id={id}",
        )

        assert response.status_code == 200

        results = response.json()
        assert results[0]['deleted'] is True
