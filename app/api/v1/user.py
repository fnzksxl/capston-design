from datetime import timedelta
from typing import List

import bcrypt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import (
  HTTPBearer,
  HTTPAuthorizationCredentials,
  OAuth2PasswordRequestForm
)
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from app import schemas, models
from app.database import get_db
from app.api.v1.utils import utils

router = APIRouter()
security = HTTPBearer()

@router.get("", response_model=List[schemas.User])
async def get_user_list(db: Session = Depends(get_db)):
  return db.query(models.User).all()

@router.post("/register", response_model=schemas.ResourceId,status_code=status.HTTP_201_CREATED)
async def add_user(data: schemas.UserAdd, db: Session = Depends(get_db)):
  row = models.User(**{'email':data.email})
  salt_value = bcrypt.gensalt()
  row.password = bcrypt.hashpw(data.password.encode(), salt_value)

  db.add(row)
  db.commit()

  return row

@router.post("/login")
async def issue_token(data: schemas.LoginUser, db: Session = Depends(get_db)):
  try:
    user = db.query(models.User).filter(models.User.email == data.email).first()
  except NoResultFound:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Wrong Information.")
  if bcrypt.checkpw(data.password.encode(), user.password.encode()): # bcrypt.checkpw가 자동으로 salt값 추출 후 서로 비교해줌
    token, user_id = await utils.create_access_token(user, exp=timedelta(minutes=30))
    return {"access_token" : token, "user_id": user_id} 
  raise HTTPException(401)

@router.post("/duplicated",status_code=status.HTTP_200_OK)
async def is_duplicated(data: schemas.DuplicatedEmail, db: Session = Depends(get_db)):
  user = db.query(models.User).filter_by(email=data.email).first()
  if user:
    return HTTPException(422,detail={"duplicated":"YES"})
  else:
    return {"duplicated":"NO"}


@router.get("/me")
async def get_current_user(cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
  if await utils.verify_user(cred):
    decoded_dict = await utils.get_username(cred,db)
    row = db.query(models.User).filter_by(id=decoded_dict.get("id")).first()
    sorted_items = sorted(row.items, key=lambda x: x.created_at, reverse=True)

    return sorted_items
  
@router.get("/is_provider/{email}")
async def is_provider_user(email: str, db: Session = Depends(get_db)):
  return True if utils.get_userprovider(db,email) else False