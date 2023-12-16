from datetime import datetime
from pydantic import BaseModel


class DuplicatedEmail(BaseModel):
    email: str


class UserAdd(DuplicatedEmail):
    password: str


class UserAddReturn(DuplicatedEmail):
    id: int


class UserPayload(UserAddReturn):
    exp: datetime
