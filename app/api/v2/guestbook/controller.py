from fastapi import Depends, APIRouter, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm.session import Session
from typing import List

from app.database import get_db
from .schema import GuestBookAdd, GuestBookReturn, GuestBookUpdate
from .service import addGuestBook, findAllGuestBook, updateGuestBook

router = APIRouter()
security = HTTPBearer()


@router.post("", response_model=GuestBookReturn, status_code=status.HTTP_201_CREATED)
async def guestbook_add(
    data: GuestBookAdd,
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    return await addGuestBook(data, cred, db)


@router.get("", response_model=List[GuestBookReturn], status_code=status.HTTP_200_OK)
async def guestbook(db: Session = Depends(get_db)):
    return await findAllGuestBook(db)


@router.put("/{id}", response_model=GuestBookReturn, status_code=status.HTTP_202_ACCEPTED)
async def guestbook_update(
    data: GuestBookUpdate,
    id: int,
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    return await updateGuestBook(data, id, cred, db)
