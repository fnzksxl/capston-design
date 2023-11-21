from pydantic import BaseModel
from datetime import datetime

class ResourceId(BaseModel):
  id: int

  class Config:
    from_attributes = True

class GetUser(BaseModel):
  id: int
  username: str

class LoginUser(BaseModel):
  email: str
  password: str

class UserAdd(BaseModel):
  email: str
  password: str

class TsItemAdd(BaseModel):
  dialect: str
  standard: str
  english: str
  chinese: str
  japanese: str

class TsItemDelete(BaseModel):
  item_id: int

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
  chinese: str
  japanese: str

class DuplicatedEmail(BaseModel):
  email: str

class GuestBookAdd(BaseModel):
  message: str
  name: str