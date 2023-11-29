from app.crud.return_code import ReturnCode


class CrudException(Exception):
    """
    CRUD에서 사용할 예외처리 기본 클래스
    """
    return_code: ReturnCode

    def __init__(self, return_code: ReturnCode):
        self.return_code = return_code

    def __str__(self) -> str:
        """
        로그에 출력할 코드 및 내용
        :return:
        """
        return str(self.return_code)
