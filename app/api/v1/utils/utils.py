import os

from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Optional

from fastapi import HTTPException
from jose import jwt
from jose.exceptions import ExpiredSignatureError

from app import models, schemas

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
bcrypt_key = SECRET_KEY.encode()

async def create_access_token(data: schemas.User, exp: Optional[timedelta] = None):
  '''
  create_access_token : DataBase 내부 정보와 입력 정보가 일치할 때 실행되며, encoded jwt 반환
  parameter : User Data, Exp (Optional)
  return type : Key(Encoded JWT)
  '''
  user_schema = schemas.User.parse_obj(data.__dict__)
  expire = datetime.utcnow() + (exp or timedelta(minutes=30))
  user_info = schemas.UserPayload(**user_schema.dict(), exp=expire)

  return jwt.encode(user_info.dict(),  SECRET_KEY, algorithm=ALGORITHM)

# get_username -> 유저 ID, 유저 Name 만 return
# get_userinfo -> 유저 is_provider return
async def get_userprovider(db,username):
  '''
  get_userprovider : 유저 테이블의 is_provider 컬럼 값 return 
  parameter : Database, UserName
  return type : is_provider(Boolean)
  '''
  is_provider = db.qeury(models.User).filter(models.User.username == username).first().is_provider

  return is_provider

async def get_username(cred,db):
  '''
  get_username : 유저 테이블의 username과 id return
  parameter : Cred 인증 정보, DataBase
  return type : ID(int), UserName(Str)
  '''
  token = cred.credentials
  try:
    decoded_data = jwt.decode(token, SECRET_KEY, ALGORITHM)
  except ExpiredSignatureError:
    raise HTTPException(401, "Expired")
  
  username = decoded_data.get('username')
  if not username:
    raise HTTPException(400, "Invalid token")
  user = db.query(models.User).filter(models.User.username == username).first()

  if not user:
    raise HTTPException(404, "User not found")
  return { 'id' : user.id, 'username' : user.username}
 
async def verify_user(cred):
  '''
  verify_user : 유저의 인증정보가 일치 -> True 반환, 아니면 HTTPExeption Raise
  parameter : Cred 인증 정보, DataBase
  return type : Boolean 
  '''
  token = cred.credentials
  try:
    if jwt.decode(token, SECRET_KEY, ALGORITHM):
      return True
  except ExpiredSignatureError:
    raise HTTPException(401, "Expired")