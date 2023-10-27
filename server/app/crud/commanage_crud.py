from sqlalchemy.orm import Session

from app.schemas.commange_schema import ComManageCreate
from app.models import commanage_model as model


def create_commanage(db: Session, commanage: ComManageCreate):
    db_data = model.ComManage(**dict(commanage))
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_commanage(db: Session):
    return (db
            .query(model.ComManage)
            .all())
