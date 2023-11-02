from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.crud import commanage_crud, user_crud
from app.schemas.commange_schema import ComManage, ComManageGet

router = APIRouter()


@router.post("/", response_model=ComManage)
def create_commanage(
        *,
        db: Session = Depends(get_db),
        commanage: ComManage
) -> Any:
    """
    commanage 객체 생성
    """
    if user := user_crud.get_user(db=db, user_id=commanage.user_id):
        return commanage_crud.create_commanage(db=db, commanage=commanage)
    else:
        raise HTTPException(status_code=404, detail=f"{commanage.user_id} is not exist user")


@router.get("/", response_model=list[ComManage])
def get_commanage(
        *,
        db: Session = Depends(get_db),
        user_id: Optional[str] = None,
        host_id: Optional[int] = None
) -> Any:
    """
    commanage 데이터 가져오기
    """
    if user_id and host_id:
        return [commanage_crud.get_commanage(db=db, user_id=user_id, host_id=host_id)]
    elif user_id:
        return commanage_crud.get_commanage_list(db=db, user_id=user_id)
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/", response_model=ComManage)
def update_commanage(
        *,
        db: Session = Depends(get_db),
        commanage: ComManageGet
) -> Any:
    """
    commanage 데이터 수정. user_id 및 host_id 가 필요하여 ComManageUpdate schema 사용
    """
    if origin_commanage := commanage_crud.get_commanage(db=db, user_id=commanage.user_id, host_id=commanage.host_id):
        return commanage_crud.update_commanage(db=db, origin=origin_commanage, update=commanage)
    else:
        raise HTTPException(status_code=404,
                            detail=f"[user : {commanage.user_id} - host_id : {commanage.host_id}] is not found")
