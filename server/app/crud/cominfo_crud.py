from sqlalchemy.orm import Session

from app.schemas.cominfo_schema import ComInfoCreate
from app.models import cominfo_model


def create_cominfo(db: Session, cominfo: ComInfoCreate):
    db_data = cominfo_model.ComInfo(**dict(cominfo))
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
