from pydantic import BaseModel


class Process(BaseModel):
    """
        프로세스 정보
    """
    pid: int
    ppid: int
    cmd_line: str
