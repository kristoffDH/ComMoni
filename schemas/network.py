from schemas.base_info import BaseInfo


class Network(BaseInfo):
    """
        네트워크 별 송수신 바이트/패킷
        bytes_sent : 송신한 바이트
        bytes_recv : 수신한 바이트
        packets_sent : 송신한 패킷
        packets_recv : 수신한 패킷

    """
    network_device_name: str
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int
