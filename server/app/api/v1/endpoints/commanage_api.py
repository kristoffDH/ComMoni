from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.commange_schema import ComManage, ComManageGet
from app.crud.commanage_crud import CommanageCRUD
from app.crud.user_crud import UserCRUD

router = APIRouter()


@router.post("/", response_model=ComManage)
def create_commanage(
        *,
        db: Session = Depends(get_db),
        commanage: ComManage
) -> ComManage:
    """
    ComManage 생성
    :param db: db Session
    :param commanage: 추가하려는 ComManage 객체
    :return: ComManage 스키마
    """
    if user := UserCRUD(db).get(user_id=commanage.user_id):
        return CommanageCRUD(db).create(commanage=commanage)
    else:
        raise HTTPException(status_code=404, detail=f"{commanage.user_id} is not exist user")


@router.get("/", response_model=list[ComManage])
def get_commanage(
        *,
        db: Session = Depends(get_db),
        user_id: Optional[str] = None,
        host_id: Optional[int] = None
) -> List[ComManage]:
    """
    User ID 또는 Host ID로 ComManage 마 가져오기 (User ID와 Host ID 둘 중, 하나는 반드시 필요)
    :param db: db Session
    :param user_id: User ID 값
    :param host_id: Host ID 값
    :return: List[ComManage] 스키마
    """
    if host_id and (commange := CommanageCRUD(db).get(host_id=host_id)):
        return [commange]
    elif user_id:
        return CommanageCRUD(db).get_all(user_id=user_id)
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/", response_model=ComManage)
def update_commanage(
        *,
        db: Session = Depends(get_db),
        commanage: ComManageGet
) -> ComManage:
    """
    ComManage 객체 수정
    :param db: db Session
    :param commanage: 수정하려는 ComManage 객체
    :return: ComManage 스키마
    """
    if origin_commanage := CommanageCRUD(db).get(host_id=commanage.host_id):
        return CommanageCRUD(db).update(origin=origin_commanage, update=commanage)
    else:
        raise HTTPException(status_code=404,
                            detail=f"[user : {commanage.user_id} - host_id : {commanage.host_id}] is not found")
