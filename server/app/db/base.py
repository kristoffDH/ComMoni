from typing import Generator, Any

from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from app.db.session import SessionLocal
from app.db.session import engine


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
