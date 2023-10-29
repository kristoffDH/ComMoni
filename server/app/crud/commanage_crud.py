from sqlalchemy.orm import Session

from app.schemas.commange_schema import ComManageUpdate, ComManage
from app.models import commanage_model as model


def create_commanage(db: Session, commanage: ComManage) -> model.ComManage:
    """
        Commanage 객체를 DB에 저장
    :param db: db 객체
    :param commanage: 저장하려는 Commanage 객체
    :return:
    """
    db_data = model.ComManage(**dict(commanage))
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_commanage_by_user(db: Session, user_id: str) -> model.ComManage:
    return (db
            .query(model.ComManage)
            .filter(model.ComManage.user_id == user_id)
            .all())


def get_commanage_by_host(db: Session, host_id: int) -> model.ComManage:
    return (db
            .query(model.ComManage)
            .filter(model.ComManage.host_id == host_id)
            .all())
