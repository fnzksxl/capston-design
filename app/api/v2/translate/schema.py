from pydantic import BaseModel


class ToTranslate(BaseModel):
    dialect: str


class Translated(ToTranslate):
    standard: str
    english: str
    chinese: str
    japanese: str
