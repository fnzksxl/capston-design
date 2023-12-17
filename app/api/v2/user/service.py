import bcrypt
from fastapi.responses import JSONResponse
from .utils import (
    add_user,
    find_user_by_email,
    create_access_token,
    is_password_correct,
    is_duplicated,
)


async def userAdd(data, db):
    salt_value = bcrypt.gensalt()
    pw = bcrypt.hashpw(data.password.encode(), salt_value)

    row = await add_user(data.email, pw, db)

    return row.as_dict()


async def userLogin(data, db):
    user = await find_user_by_email(data.email, db)
    if await is_password_correct(data.password, user.password):
        token, user_id = await create_access_token(user)
        return JSONResponse(content={"user_id": user_id}, headers={"access_token": token})


async def emailDuplicated(data, db):
    return {"duplicated": await is_duplicated(data.email, db)}
