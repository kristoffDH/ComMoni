from schemas.base_info import BaseInfo


class Disk(BaseInfo):
    """
        디스크 총 사이즈와 현재 사용 중인 사이즈
        total : 전체 디스크 용량
        used : 현재 사용 중인 디스크 용량
    """
    total: int
    used: int
