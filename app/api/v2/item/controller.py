from fastapi import Depends, APIRouter, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm.session import Session

from app.database import get_db
from .schema import TsItemAdd, TsItem
from .service import addTsItem

router = APIRouter()
security = HTTPBearer()


@router.post("/add", response_model=TsItem, status_code=status.HTTP_201_CREATED)
async def add_item(
    data: TsItemAdd,
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    return await addTsItem(data, cred, db)
