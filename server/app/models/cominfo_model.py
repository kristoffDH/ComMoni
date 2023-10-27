from sqlalchemy import Column, Integer, DateTime, Float

from app.db.base import Base


class ComInfo(Base):
    """
        모니터링 데이터 모델

        Attributes:
            id : 데이터 id(AutoIncrement)
            server_id : 모니터링 시스템에 등록된 모니터링 대상 ID
            cpu_utilization : cpu 사용률
            memory_utilization : 메모리 사용률
            disk_utilization : 디스크 사용률
            make_datetime : 데이터 생성 날짜/시간
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer)
    cpu_utilization = Column(Float)
    memory_utilization = Column(Float)
    disk_utilization = Column(Float)
    make_datetime = Column(DateTime)
