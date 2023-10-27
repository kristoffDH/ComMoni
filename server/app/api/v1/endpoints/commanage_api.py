from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.commange_schema import ComManageCreate, ComManage
from app.crud import commanage_crud

router = APIRouter()


@router.post("/", response_model=ComManageCreate)
def create_commanage(
        *,
        db: Session = Depends(get_db),
        commanage: ComManageCreate
) -> Any:
    return commanage_crud.create_commanage(db=db, commanage=commanage)


@router.get("/all", response_model=list[ComManage])
def get_commanage(
        *,
        db: Session = Depends(get_db)
) -> Any:
    commanages = commanage_crud.get_commanage(db=db)
    return commanages
