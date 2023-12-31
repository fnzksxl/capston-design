from fastapi import Depends, APIRouter, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm.session import Session
from typing import List

from app.database import get_db
from .schema import TsItemAdd, TsItem, TsItemDelete
from .service import addTsItem, findTsItems, deleteTsItem

router = APIRouter()
security = HTTPBearer()


@router.get("", response_model=List[TsItem])
async def get_item_list(db: Session = Depends(get_db)):
    return await findTsItems(db)


@router.post("", response_model=TsItem, status_code=status.HTTP_201_CREATED)
async def add_item(
    data: TsItemAdd,
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    return await addTsItem(data, cred, db)


@router.delete("/{id}", response_model=TsItemDelete, status_code=status.HTTP_202_ACCEPTED)
async def delete_item(
    id: int,
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    return await deleteTsItem(id, cred, db)
