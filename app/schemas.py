from pydantic import BaseModel
from datetime import datetime

class ResourceId(BaseModel):
  id: int

  class Config:
    from_attributes = True

class GetUser(BaseModel):
  id: int
  username: str

class UserAdd(BaseModel):
  email: str
  username: str
  password: str

class TsItemAdd(BaseModel):
  dialect: str
  standard: str
  english: str

class TsItem(TsItemAdd):
  id: int
  owner_id: int

  class Config:
    from_attributes = True

class User(UserAdd):
  is_provider: bool
  id: int
  items: list[TsItem] = []

  class Config:
    from_attributes = True

class UserPayload(User):
  exp: datetime

class ToTranslate(BaseModel):
  dialect:str

class Translated(ToTranslate):
  standard: str
  english: str