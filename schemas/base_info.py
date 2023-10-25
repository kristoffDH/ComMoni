from pydantic import BaseModel
from typing import Optional


class BaseInfo(BaseModel):
    """
        수집 정보에서 기본으로 가지고 있어야할 정보
        device_id : 등록된 아이디
        device_name : 등록된 이름
    """
    server_id: int
    server_name: Optional[str] = None
