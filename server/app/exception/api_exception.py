from fastapi import status


class APIExceptionBase(Exception):
    """
    API Exception 처리를 위한 베이스 클래스
    Attributes:
        - status : http status code
        - message : 상세 내용
    """
    status: int
    message: str

    def __init__(self, http_status: int, message: str):
        self.http_status = http_status
        self.message = message

    def make_content(self) -> dict:
        """
        클라이언트로 전달할 응답용 content 생성
        :return:
        """
        return {"message": self.message}


class UserNotFound(APIExceptionBase):
    """
    User 가 없을때 처리할 예외 클래스
    """

    def __init__(self, user_id: str):
        super().__init__(http_status=status.HTTP_404_NOT_FOUND,
                         message=f"{user_id} is not existed.")


class AlreadyExistedUser(APIExceptionBase):
    """
    User 가 이미 존재할 때 처리할 예외 클래스
    """

    def __init__(self, user_id: str):
        super().__init__(http_status=status.HTTP_409_CONFLICT,
                         message=f"{user_id} is already existed.")


class ItemNotFound(APIExceptionBase):
    """
    Get요청에 대한 결과값이 없을 때 처리할 예외 클래스
    """

    def __init__(self):
        super().__init__(http_status=status.HTTP_404_NOT_FOUND,
                         message="Item not Found.")


class HostNotFound(APIExceptionBase):
    """
    User 가 없을때 처리할 예외 클래스
    """

    def __init__(self, host_id: int):
        super().__init__(http_status=status.HTTP_404_NOT_FOUND,
                         message=f"{host_id} is not existed.")


class ServerError(APIExceptionBase):
    """
    서버 내에서 오류가 발생 했을 때 처리할 예외 클래스
    """

    def __init__(self, err_message: str):
        super().__init__(http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                         message=f"Server error. Internal err code : {err_message}")


__all__ = (
    "UserNotFound",
    "AlreadyExistedUser",
    "ItemNotFound",
    "HostNotFound",
    "ServerError"
)