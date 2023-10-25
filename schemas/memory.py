from schemas.base_info import BaseInfo


class Memory(BaseInfo):
    """
        총 메모리와 현재 사용 중인 메모리
        total : 전체 메모리 용량
        used : 현재 사용 중인 메모리 용량
    """
    total: int
    used: int
