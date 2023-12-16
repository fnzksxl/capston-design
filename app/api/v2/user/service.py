import bcrypt

from .utils import add_user


async def userAdd(data, db):
    salt_value = bcrypt.gensalt()
    pw = bcrypt.hashpw(data.password.encode(), salt_value)

    row = await add_user(data.email, pw, db)

    return row.as_dict()
