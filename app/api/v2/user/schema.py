from datetime import datetime
from pydantic import BaseModel


class UserAdd(BaseModel):
    email: str
    password: str


class UserAddReturn(BaseModel):
    email: str
    id: int


class UserPayload(UserAddReturn):
    exp: datetime
