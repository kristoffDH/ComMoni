from schemas.base_info import BaseInfo


class Cpu(BaseInfo):
    """
        현재 사용중인 CPU 퍼센트
        used : 현재 CPU 사용률
    """
    used: float
