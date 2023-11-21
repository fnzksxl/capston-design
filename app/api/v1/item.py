from typing import List

from sqlalchemy.orm.session import Session

from fastapi import Depends, APIRouter, status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer

from app import models, schemas
from app.database import get_db

from app.api.v1.utils import utils

router = APIRouter()
security = HTTPBearer()

@router.get("", response_model=List[schemas.TsItem])
async def get_item_list(db: Session = Depends(get_db)):
  return db.query(models.TsItem).all()

@router.post("/add", response_model=schemas.ResourceId,status_code=status.HTTP_201_CREATED)
async def add_item(data: schemas.TsItemAdd, cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
  if await utils.verify_user(cred):
    user_info = await utils.get_username(cred,db)
    row = models.TsItem(**data.dict(),owner_id=user_info.get('id'))
    db.add(row)
    db.commit()
    
    return row
  
@router.post("/delete",status_code=status.HTTP_202_ACCEPTED)
async def delete_item(data: schemas.TsItemDelete, cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
  if await utils.verify_user(cred):
    print(data)
    item_info = db.query(models.TsItem).filter_by(id=data.item_id).first()
    db.delete(item_info)
    db.commit()

    return {"success":True}
