from sqlalchemy import Column, Integer, DateTime, Float

from app.db.base import Base


class ComInfo(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer)
    cpu_utilization = Column(Float)
    memory_utilization = Column(Float)
    disk_utilization = Column(Float)
    make_datetime = Column(DateTime)
