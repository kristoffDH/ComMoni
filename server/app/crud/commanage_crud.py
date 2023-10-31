from typing import Any
from sqlalchemy.orm import Session

from app.schemas.commange_schema import ComManageGet, ComManage
from app.models import commanage_model as model


def create_commanage(db: Session, commanage: ComManage) -> Any:
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


def get_commanage_list(db: Session, user_id: str) -> Any:
    """
    유저 한명은 여러개의 commanage를 가질 수 있음으로 여러 Commanage 반환
    """
    return (db
            .query(model.ComManage)
            .filter(model.ComManage.user_id == user_id)
            .all())


def get_commanage(db: Session, user_id: str, host_id: int) -> ComManageGet:
    """
    user_id 및 host_id로 특정 commanage 가져오기
    """
    return (db
            .query(model.ComManage)
            .filter(model.ComManage.user_id == user_id, model.ComManage.host_id == host_id)
            .first())


def update_commanage(db: Session, origin: ComManageGet, update: ComManageGet) -> Any:
    """
    commange 데이터 수정
    """
    update_data = dict(update)
    for key, value in update_data.items():
        setattr(origin, key, value)

    db.add(origin)
    db.commit()
    db.refresh(origin)
    return origin
