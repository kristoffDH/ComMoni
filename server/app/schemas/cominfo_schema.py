from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ComInfoBase(BaseModel):
    server_id: int
    make_datetime: datetime
    cpu_utilization: Optional[float] = None
    memory_utilization: Optional[float] = None
    disk_utilization: Optional[float] = None


class ComInfoCreate(ComInfoBase):
    pass

    class Config:
        from_attributes = True
