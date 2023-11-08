from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    """
        Attributes
            - user_id : 사용자 아이디
            - user_pw : 사용자 비밀번호
            - user_name : 사용자 이름
    """
    user_id: Optional[str] = None
    user_pw: Optional[str] = None
    user_name: Optional[str] = None
    deleted: Optional[bool] = None

    class Config:
        from_attributes = True


class User(UserBase):
    pass


class UserCreate(UserBase):
    user_id: str
    user_pw: str


class UserUpdate(UserBase):
    user_id: str
    user_pw: str


class UserDelete(UserBase):
    user_id: str
