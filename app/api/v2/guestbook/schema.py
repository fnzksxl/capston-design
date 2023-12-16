from pydantic import BaseModel


class GuestBookAdd(BaseModel):
    message: str
    message_owner: str


class GuestBookReturn(GuestBookAdd):
    id: int
    owner_id: int


class GuestBookUpdate(BaseModel):
    message: str
    id: int
