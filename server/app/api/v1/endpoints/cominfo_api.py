from typing import Any, Annotated, Union
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.crud import cominfo_crud, commanage_crud
from app.schemas.cominfo_schema import ComInfoCreate, ComInfoGet

router = APIRouter()


@router.post("/", response_model=ComInfoCreate)
def create_cominfo(
        *,
        db: Session = Depends(get_db),
        cominfo: ComInfoCreate
) -> Any:
    if commanage_crud.get_commanage_by_host(db=db, host_id=cominfo.host_id):
        return cominfo_crud.create_cominfo(db=db, cominfo=cominfo)
    else:
        raise HTTPException(status_code=404, detail=f"host_id[{cominfo.host_id}] is not exist host_id")


@router.get("/", response_model=list[ComInfoGet])
def get_cominfos(
        *,
        db: Session = Depends(get_db),
        host_id: int,
        skip: int = 0,
        limit: int = 1000,
        start_dt: datetime = None,
        end_dt: datetime = None
) -> Any:
    if start_dt and end_dt:
        cominfos = cominfo_crud.get_cominfo_by_datetime(db=db, host_id=host_id, start_dt=start_dt, end_dt=end_dt)
    else:
        cominfos = cominfo_crud.get_multi_cominfo(db=db, host_id=host_id, skip=skip, limit=limit)

    if cominfos:
        return cominfos
    else:
        raise HTTPException(status_code=404, detail="Item not found")
