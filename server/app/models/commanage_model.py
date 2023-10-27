from sqlalchemy import Column, Integer, String

from app.db.base import Base


class ComManage(Base):
    """
        모니링 서버 정보 모델

        Attributes:
            server_id : 모니터링 서버 ID
            server_name : 서버 이름
            server_ip : 서버 아이피
            server_memory : 서버 총 메모리
            server_disk : 서버 총 디스크
    """
    server_id = Column(Integer, primary_key=True, autoincrement=True)
    server_name = Column(String(50))
    server_ip = Column(String(16))
    server_memory = Column(String(20))
    server_disk = Column(String(20))
