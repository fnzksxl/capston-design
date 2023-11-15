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

from app import schemas, models
from app.database import get_db
from app.api.v1.utils import utils

router = APIRouter()
security = HTTPBearer()

@router.get("", response_model=List[schemas.User])
async def get_user_list(db: Session = Depends(get_db)):
  return db.query(models.User).all()

@router.post("/add", response_model=schemas.ResourceId,status_code=status.HTTP_201_CREATED)
async def add_user(data: schemas.UserAdd, db: Session = Depends(get_db)):
  row = models.User(**{'email':data.email,'username':data.username})
  salt_value = bcrypt.gensalt()
  row.password = bcrypt.hashpw(data.password.encode(), salt_value)

  db.add(row)
  db.commit()

  return row

@router.post("/login")
async def issue_token(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.username == data.username).first()
  if bcrypt.checkpw(data.password.encode(), user.password.encode()): # bcrypt.checkpw가 자동으로 salt값 추출 후 서로 비교해줌
    return await utils.create_access_token(user, exp=timedelta(minutes=30))
  raise HTTPException(401)


@router.get("/me", response_model=schemas.GetUser)
async def get_current_user(cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
  user_info = await utils.get_username(cred,db)
  return user_info

@router.post("/is_provider")
async def is_provider_user(username: str, db: Session = Depends(get_db)):
  return True if utils.get_userprovider(db,username) else False