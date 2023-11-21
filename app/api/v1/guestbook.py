from fastapi import Depends, APIRouter, status,HTTPException
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from sqlalchemy.orm.session import Session

from app import models, schemas
from app.database import get_db

from app.api.v1.utils import utils

router = APIRouter()
security = HTTPBearer()

@router.post("/add",status_code=status.HTTP_201_CREATED)
async def guestbook_add(data: schemas.GuestBookAdd, cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
  decoded_dict = await utils.verify_user(cred)
  if decoded_dict:
    guestbook_row = models.GuestBook(message=data.message,owner_id=decoded_dict.get("id"),message_owner=data.name)
    db.add(guestbook_row)
    db.commit()

    return {"SUCCESS":True}
  
  else:
    raise HTTPException(422)
  
@router.get("",status_code=status.HTTP_200_OK)
async def guestbook(db: Session=Depends(get_db)):
  guestbook_row = db.query(models.GuestBook).all()
  sorted_items = sorted(guestbook_row, key=lambda x: x.created_at, reverse=True)
  return sorted_items