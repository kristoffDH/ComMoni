from typing import Optional

from pydantic import BaseModel


class ComManageBase(BaseModel):
    server_name: Optional[str] = None
    server_ip: Optional[str] = None
    server_memory: Optional[str] = None
    server_disk: Optional[str] = None


class ComManage(ComManageBase):
    class Config:
        from_attributes = True


class ComManageCreate(ComManageBase):
    class Config:
        from_attributes = True
