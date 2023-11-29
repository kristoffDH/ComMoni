from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import func

from app.db.base import Base


class RefreshToken(Base):
    """
        Refrest Token

        Attributes

    """
    no = Column(Integer, primary_key=True, autoincrement=True)
    refresh_token = Column(String)
    make_datetime = Column(DateTime, server_default=func.now())
