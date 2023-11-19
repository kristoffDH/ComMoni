from urllib import parse

from app.tests.api.conftest import client

from app.tests.api.v1.endpoints.api_confest import create_user, create_commanage

host_id = 1


def test_create_cominfo(client, create_user, create_commanage):
    """
    cominfo 생성 테스트
    """

    for id in range(1, 55):
        response = client.post(
            "/api/v1/cominfo",
            json={
                "host_id": host_id,
                "cpu_utilization": id,
                "memory_utilization": id,
                "disk_utilization": id,
                "make_datetime": f"2023-11-01T01:01:{id:02}",
            },
        )

        assert response.status_code == 201


def test_get_cominfo_1(client):
    """
    cominfo get test
    """

    # 가져오기. limit 기본값은 50
    response = client.get(
        f"/api/v1/cominfo?host_id={host_id}"
    )

    assert response.status_code == 200
    assert len(response.json()) == 50


def test_get_cominfo_2(client):
    """
    cominfo get test
    """

    # 가져오기. limit 기본값은 50
    response = client.get(
        f"/api/v1/cominfo?host_id={host_id}"
    )

    assert response.status_code == 200
    assert len(response.json()) == 50


def test_get_cominfo_3(client):
    """
    cominfo get test
    """

    # test skip, limit param
    skip = 0
    limit = 5
    response = client.get(
        f"/api/v1/cominfo?host_id={host_id}&skip={skip}&limit={limit}"
    )

    assert response.status_code == 200
    assert len(response.json()) == 5


def test_get_cominfo_4(client):
    """
    cominfo get test
    """

    # test skip, limit param
    skip = 1
    limit = 3
    response = client.get(
        f"/api/v1/cominfo?host_id={host_id}&skip={skip}&limit={limit}"
    )

    assert response.status_code == 200
    data_list = response.json()
    assert len(data_list) == 3
    # 테스트 데이터 생성시 row 값과 동일하게 생성했기 때문에 1스킵하면 2.0부터 시작
    assert data_list[0]["cpu_utilization"] == 2.0
    assert data_list[1]["cpu_utilization"] == 3.0
    assert data_list[2]["cpu_utilization"] == 4.0


def test_get_cominfo_by_datetime_1(client):
    """
    cominfo get test by datetime
    start_dt, end_dt 둘다 있는 경우
    """
    start_dt = "2023-11-01T01:01:01"
    end_dt = "2023-11-01T01:01:30"
    dt_param = f"start_dt={parse.quote(start_dt)}&end_dt={parse.quote(end_dt)}"
    api_path = f"/api/v1/cominfo?host_id={host_id}&{dt_param}"

    response = client.get(api_path)

    assert response.status_code == 200
    result = response.json()
    assert len(result) == 30
    assert result[0]["make_datetime"] == start_dt
    assert result[-1]["make_datetime"] == end_dt


def test_get_cominfo_by_datetime_2(client):
    """
    cominfo get test by datetime
    start_dt 만 있는 경우
    """
    start_dt = "2023-11-01T01:01:15"
    end_dt = "2023-11-01T01:01:54"
    dt_param = f"start_dt={parse.quote(start_dt)}"
    api_path = f"/api/v1/cominfo?host_id={host_id}&{dt_param}"

    response = client.get(api_path)
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 40
    assert result[0]["make_datetime"] == start_dt
    assert result[-1]["make_datetime"] == end_dt


def test_get_cominfo_by_datetime_3(client):
    """
    cominfo get test by datetime
    end_dt 만 있는 경우
    """
    start_dt = "2023-11-01T01:01:01"
    end_dt = "2023-11-01T01:01:30"
    dt_param = f"end_dt={parse.quote(end_dt)}"
    api_path = f"/api/v1/cominfo?host_id={host_id}&{dt_param}"

    response = client.get(api_path)
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 30
    assert result[0]["make_datetime"] == start_dt
    assert result[-1]["make_datetime"] == end_dt


def test_put_cominfo_rt(client):
    """
    cominfo rt put[create] test

    """

    # 최초 등록 전 404 확인
    response = client.get(
        f"/api/v1/cominfo/realtime/{host_id}"
    )

    assert response.status_code == 404

    # create cominfo rt
    response = client.put(
        "/api/v1/cominfo/realtime",
        json={
            "host_id": host_id,
            "cpu_utilization": 15.0,
            "memory_utilization": 25.0,
            "disk_utilization": 35.0,
        },
    )

    assert response.status_code == 204

    # get
    response = client.get(
        f"/api/v1/cominfo/realtime/{host_id}"
    )

    assert response.status_code == 200
    result = response.json()
    assert result["host_id"] == host_id
    assert result["cpu_utilization"] == 15.0
    assert result["memory_utilization"] == 25.0
    assert result["disk_utilization"] == 35.0
    assert result["make_datetime"] is not ""

    # put cominfo rt
    response = client.put(
        "/api/v1/cominfo/realtime",
        json={
            "host_id": host_id,
            "cpu_utilization": 45.0,
            "memory_utilization": 55.0,
            "disk_utilization": 65.0,
        },
    )

    assert response.status_code == 204

    # get
    response = client.get(
        f"/api/v1/cominfo/realtime/{host_id}"
    )

    assert response.status_code == 200
    result = response.json()
    assert result["host_id"] == host_id
    assert result["cpu_utilization"] == 45.0
    assert result["memory_utilization"] == 55.0
    assert result["disk_utilization"] == 65.0
    assert result["update_datetime"] is not ""
