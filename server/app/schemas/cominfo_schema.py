from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ComInfoBase(BaseModel):
    server_id: int
    make_datetime: Optional[datetime] = None
    cpu_utilization: Optional[float] = None
    memory_utilization: Optional[float] = None
    disk_utilization: Optional[float] = None


class ComInfo(ComInfoBase):
    class Config:
        from_attributes = True


class ComInfoCreate(ComInfoBase):
    make_datetime: datetime

    class Config:
        from_attributes = True
