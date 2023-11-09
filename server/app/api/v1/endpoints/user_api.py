from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.crud.user_crud import UserCRUD
from app.schemas.user_schema import UserCreate, User, UserUpdate, UserDelete
from app.crud.commanage_crud import CommanageCRUD

from app.exception.api_exception import UserNotFoundException

router = APIRouter()


@router.post("/", response_model=UserCreate)
def create_user(
        *,
        db: Session = Depends(get_db),
        user: UserCreate
) -> User:
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
    user = UserCRUD(db).get(user_id=user_id)

    if not user:
        raise UserNotFoundException(user_id=user_id)

    if user.deleted:
        raise HTTPException(status_code=404, detail=f"{user_id} is deleted")
    else:
        return user


@router.put("/")
def update_user(
        *,
        db: Session = Depends(get_db),
        user: UserUpdate
) -> Any:
    """
    User 객체 정보 수정
    :param db: db Session
    :param user: 수정하려는 유저 정보
    :return: User 스키마
    """
    UserCRUD(db).update(update_data=user)


@router.delete("/")
def delete_user(
        *,
        db: Session = Depends(get_db),
        user: UserDelete
) -> Any:
    """
    User를 삭제
    :param db: db Session
    :param user: 삭제하려는 유저 정보
    :return:
    """

    if not UserCRUD(db).get(user_id=user.user_id):
        raise HTTPException(status_code=404, detail=f"{user.user_id} is not exist")

    # User ID 에 해당하는 ComManage 전부 삭제 처리
    CommanageCRUD(db).delete_all(user_id=user.user_id)

    # user delete
    UserCRUD(db).delete(user_id=user.user_id)
