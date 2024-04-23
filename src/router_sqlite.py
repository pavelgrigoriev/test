from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models_sqlite import User
from schemas import UserSchema
from sqlite import SessionLocal


router = APIRouter(
    prefix="/users"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add_user/")
def add_user(user: UserSchema, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/get_users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.put("/update_user/{user_id}")
def update_user(user_id: int, user_data: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user_data.dict().items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/get_user/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()