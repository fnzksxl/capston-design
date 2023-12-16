from pydantic import BaseModel


class TsItemAdd(BaseModel):
    dialect: str
    standard: str
    english: str
    chinese: str
    japanese: str


class TsItem(TsItemAdd):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class TsItemDelete(BaseModel):
    id: int
