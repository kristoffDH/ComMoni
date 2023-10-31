from typing import Any
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, User, UserUpdate
from app.models import user_model as model


def create_user(db: Session, user: UserCreate) -> User:
    """
    User 데이터 생성
    """
    db_data = model.User(**dict(user))
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_user(db: Session, user_id: str) -> User:
    """
    User 데이터 가져오기
    """
    return (db
            .query(model.User)
            .filter(model.User.user_id == user_id)
            .first())


def update_user(db: Session, origin: User, update: UserUpdate) -> User:
    """
    User 데이터 수정
    """
    update_data = dict(update)
    for key, value in update_data.items():
        setattr(origin, key, value)

    db.add(origin)
    db.commit()
    db.refresh(origin)
    return origin
