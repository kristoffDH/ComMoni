from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.cominfo_schema import ComInfoCreate
from app.crud import cominfo_crud

router = APIRouter()


@router.post("/", response_model=ComInfoCreate)
def create_cominfo(
        *,
        db: Session = Depends(get_db),
        cominfo: ComInfoCreate
) -> Any:
    return cominfo_crud.create_cominfo(db=db, cominfo=cominfo)
