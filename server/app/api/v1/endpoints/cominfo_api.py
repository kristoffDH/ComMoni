from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.cominfo_schema import ComInfoCreate, ComInfo
from app.crud import cominfo_crud

router = APIRouter()


@router.post("/", response_model=ComInfoCreate)
def create_cominfo(
        *,
        db: Session = Depends(get_db),
        cominfo: ComInfoCreate
) -> Any:
    return cominfo_crud.create_cominfo(db=db, cominfo=cominfo)


@router.get("/{server_id}", response_model=list[ComInfo])
def get_cominfos(
        *,
        db: Session = Depends(get_db),
        server_id: int
) -> Any:
    cominfos = cominfo_crud.get_cominfo(db=db, server_id=server_id)
    return cominfos
