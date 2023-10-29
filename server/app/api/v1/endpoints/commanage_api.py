from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.crud import commanage_crud, user_crud
from app.schemas.commange_schema import ComManage
from app.schemas.user_schema import User

router = APIRouter()


@router.post("/", response_model=ComManage)
def create_commanage(
        *,
        db: Session = Depends(get_db),
        commanage: ComManage
) -> Any:
    if user := user_crud.get_user(db=db, user_id=commanage.user_id):
        return commanage_crud.create_commanage(db=db, commanage=commanage)
    else:
        raise HTTPException(status_code=404, detail=f"{commanage.user_id} is not exist user")


@router.get("/", response_model=list[ComManage])
def get_commanage(
        *,
        db: Session = Depends(get_db),
        user_id: str
) -> Any:
    if commanages := commanage_crud.get_commanage_by_user(db=db, user_id=user_id):
        return commanages
    else:
        raise HTTPException(status_code=404, detail="Item not found")
