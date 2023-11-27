from enum import IntEnum


class ReturnCode(IntEnum):
    """
    crud 모듈에서 사용할 반환 코드
    """

    DB_OK = 0
    DB_CREATE_ERROR = 1
    DB_UPDATE_NONE = 2
    DB_UPDATE_ERROR = 3
    DB_DELETE_NONE = 4
    DB_DELETE_ERROR = 5
