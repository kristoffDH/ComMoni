from typing import Optional

from pydantic import BaseModel


class ComManageBase(BaseModel):
    """
        Attributes
            - host_id : 호스트 아이디
            - user_id : 사용자 아이디
            - host_name : 호스트 이름
            - host_ip : 호스트 아이피
            - memory : 메모리 용량
            - disk : 디스크 용량
    """
    host_id: Optional[int] = None
    user_id: Optional[int] = None
    host_name: Optional[str] = None
    host_ip: Optional[str] = None
    memory: Optional[str] = None
    disk: Optional[str] = None

    class Config:
        from_attributes = True


class ComManage(ComManageBase):
    pass


class ComManageCreate(ComManageBase):
    host_id: int


class ComManageUpdate(ComManageBase):
    host_id: int
    user_id: int
