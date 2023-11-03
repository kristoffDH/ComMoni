from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.crud import user_crud
from app.schemas.user_schema import UserCreate, User, UserUpdate

router = APIRouter()


@router.post("/", response_model=UserCreate)
def create_user(
        *,
        db: Session = Depends(get_db),
        user: UserCreate
) -> Any:
    if user_crud.get_user(db=db, user_id=user.user_id):
        raise HTTPException(status_code=404, detail="ID is already used")
    else:
        return user_crud.create_user(db=db, user=user)


@router.get("/", response_model=User)
def get_user(
        *,
        db: Session = Depends(get_db),
        user_id: str
) -> Any:
    if user := user_crud.get_user(db=db, user_id=user_id):
        return user
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/", response_model=User)
def update_user(
        *,
        db: Session = Depends(get_db),
        user: UserUpdate
) -> Any:
    """
    User 데이터 수정
    """
    if origin_user := user_crud.get_user(db=db, user_id=user.user_id):
        return user_crud.update_user(db=db, origin=origin_user, update=user)
    else:
        raise HTTPException(status_code=404, detail=f"[user : {user.user_id} is not found")