from sqlalchemy.orm.session import Session

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer

from app import models, schemas
from app.database import get_db

from app.AI import test
from app.api.v1.utils import utils

router = APIRouter()
security = HTTPBearer()

@router.post("",response_model=schemas.Translated)
async def translate_item(data: schemas.ToTranslate,cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
  if utils.verify_user(cred):
    translated_text = test.generate_text(data.dialect)[0] # Translation
    english_text = test.get_koen_text(translated_text)

    return {"dialect": data.dialect, "standard": translated_text, "english": english_text}
  
  return HTTPException(501, "User not verified")