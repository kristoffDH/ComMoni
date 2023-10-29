from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, User
from app.models import user_model as model


def create_user(db: Session, user: UserCreate) -> model.User:
    db_data = model.User(**dict(user))
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_user(db: Session, user_id: str) -> model.User:
    return (db
            .query(model.User)
            .filter(model.User.user_id == user_id)
            .first())
