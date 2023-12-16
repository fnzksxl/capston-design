from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm.session import Session

from app.database import get_db
from .schema import UserAdd, UserAddReturn
from .service import userAdd, userLogin

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserAddReturn, status_code=status.HTTP_201_CREATED)
async def add_user(data: UserAdd, db: Session = Depends(get_db)):
    return await userAdd(data, db)


@router.post("/login")
async def issue_token(data: UserAdd, db: Session = Depends(get_db)):
    return await userLogin(data, db)
