import bcrypt

from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import ExpiredSignatureError

from app.config import settings
from app.models import User
from .schema import UserPayload


async def add_user(email, pw, db):
    try:
        row = User(**{"email": email, "password": pw})
        db.add(row)
        db.commit()

        return row
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{e} occured while registering",
        )


async def find_user_by_email(email, db):
    row = db.query(User).filter_by(email=email).first()
    if row:
        return row
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No Email Found",
        )


async def is_password_correct(data, user):
    if bcrypt.checkpw(data.encode(), user.encode()):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect Password",
        )


async def create_access_token(user):
    user_schema = user.as_dict()
    expire = datetime.utcnow() + timedelta(days=1)
    user_info = UserPayload(**user_schema, exp=expire)

    return (
        jwt.encode(user_info.dict(), settings.SECRET_KEY, algorithm=settings.ALGORITHM),
        user_schema["id"],
    )


async def is_duplicated(email, db):
    if db.query(User).filter_by(email=email).first():
        return True
    else:
        return False


async def verify_user(cred):
    token = cred.credentials
    try:
        jwt_dict = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        if jwt_dict:
            return jwt_dict
    except ExpiredSignatureError:
        raise HTTPException(401, "Expired")
