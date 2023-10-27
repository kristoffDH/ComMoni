from sqlalchemy.orm import Session

from app.schemas.cominfo_schema import ComInfoCreate
from app.models import cominfo_model as model


def create_cominfo(db: Session, cominfo: ComInfoCreate):
    db_data = model.ComInfo(**dict(cominfo))
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_cominfo(db: Session, server_id: int):
    return (db
            .query(model.ComInfo)
            .filter(model.ComInfo.server_id == server_id)
            .all())
