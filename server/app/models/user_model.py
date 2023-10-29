from sqlalchemy import Column, Integer, String

from app.db.base import Base


class User(Base):
    """
        사용자 객체 모델

        Attributes
            - user_id : 사용자 아이디
            - user_pw : 사용자 비밀번호
            - user_name : 사용자 이름
    """
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_pw = Column(String)
    user_name = Column(String)
