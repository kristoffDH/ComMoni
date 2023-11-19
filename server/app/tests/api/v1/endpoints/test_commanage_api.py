from app.tests.api.conftest import client

from app.tests.api.v1.endpoints import api_confest
from app.tests.api.v1.endpoints.api_confest import create_user


def test_create_commanage(client, create_user):
    """
    commanage 생성 테스트
    """

    response = client.post(
        "/api/v1/commanage",
        json={"user_id": api_confest.user_id,
              "host_name": api_confest.host_name,
              "host_ip": api_confest.host_ip,
              "memory": api_confest.host_memory,
              "disk": api_confest.host_disk
              },
    )

    assert response.status_code == 201
    assert response.json() == {"host_id": 1}

    response = client.post(
        "/api/v1/commanage",
        json={"user_id": api_confest.user_id,
              "host_name": api_confest.host_name_2,
              "host_ip": api_confest.host_ip,
              "memory": api_confest.host_memory,
              "disk": api_confest.host_disk
              },
    )

    assert response.status_code == 201
    assert response.json() == {"host_id": 2}


def test_get_commanage(client):
    """
    commanage get 테스트
    """

    # get comamage by host_id
    check_host_id = 1
    response = client.get(
        f"/api/v1/commanage?host_id={check_host_id}",
    )

    assert response.status_code == 200
    assert response.json() == [{
        'user_id': api_confest.user_id,
        'host_id': 1,
        'host_name': api_confest.host_name,
        'host_ip': api_confest.host_ip,
        'memory': api_confest.host_memory,
        'disk': api_confest.host_disk,
        'deleted': False}]

    # get commanage by user
    check_user_id = api_confest.user_id
    response = client.get(
        f"/api/v1/commanage?user_id={api_confest.user_id}",
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            'user_id': api_confest.user_id,
            'host_id': 1,
            'host_name': api_confest.host_name,
            'host_ip': api_confest.host_ip,
            'memory': api_confest.host_memory,
            'disk': api_confest.host_disk,
            'deleted': False},
        {
            'user_id': api_confest.user_id,
            'host_id': 2,
            'host_name': api_confest.host_name_2,
            'host_ip': api_confest.host_ip,
            'memory': api_confest.host_memory,
            'disk': api_confest.host_disk,
            'deleted': False}
    ]


def test_update_commanage(client):
    """
    commanage update 테스트
    """
    update_host_name = "update_name"
    update_ip = "192.168.1.1"
    update_memory = "32G"
    update_disk = "1T"

    response = client.put(
        "/api/v1/commanage",
        json={
            "host_id": 1,
            "host_name": update_host_name,
            "host_ip": update_ip,
            "memory": update_memory,
            "disk": update_disk
        },
    )

    assert response.status_code == 204

    # update check
    # get commanage by user
    check_host_id = 1
    response = client.get(
        f"/api/v1/commanage?host_id={check_host_id}",
    )

    assert response.status_code == 200
    assert response.json() == [{
        'user_id': api_confest.user_id,
        'host_id': check_host_id,
        "host_name": update_host_name,
        "host_ip": update_ip,
        "memory": update_memory,
        "disk": update_disk,
        'deleted': False}]


def test_delete_commanage(client):
    """
    delete commanage 테스트
    """
    delete_host_id = 1
    response = client.delete(
        f"/api/v1/commanage/{delete_host_id}",
    )

    assert response.status_code == 204

    # delete check
    # get commanage by user
    check_host_id = 1
    response = client.get(
        f"/api/v1/commanage?host_id={check_host_id}",
    )

    assert response.status_code == 200

    results = response.json()
    assert results[0]['deleted'] is True
