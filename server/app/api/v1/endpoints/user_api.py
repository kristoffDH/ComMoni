from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.user_schema import UserCreate, User, UserUpdate
from app.crud.user_crud import UserCRUD

router = APIRouter()


@router.post("/", response_model=UserCreate)
def create_user(
        *,
        db: Session = Depends(get_db),
        user: UserCreate
) -> UserCreate:
    """
    유저 생성
    :param db: db Session
    :param user: 추가하려는 User 객체
    :return: UserCreate 스키마
    """
    if UserCRUD(db).get(user_id=user.user_id):
        raise HTTPException(status_code=404, detail="ID is already used")
    else:
        return UserCRUD(db).create(user=user)


@router.get("/", response_model=User)
def get_user(
        *,
        db: Session = Depends(get_db),
        user_id: str
) -> User:
    """
    User ID 값으로 User 값 가져오기
    :param db: db Session
    :param user_id: 찾으려고하는 유저 아이디
    :return: User 스키마
    """
    if user := UserCRUD(db).get(user_id=user_id):
        return user
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/", response_model=User)
def update_user(
        *,
        db: Session = Depends(get_db),
        user: UserUpdate
) -> User:
    """
    User 객체 정보 수정
    :param db: db Session
    :param user: 수정하려는 유저 정보
    :return: User 스키마
    """
    if origin_user := UserCRUD(db).get(user_id=user.user_id):
        return UserCRUD(db).update(origin=origin_user, update=user)
    else:
        raise HTTPException(status_code=404, detail=f"[user : {user.user_id} is not found")
