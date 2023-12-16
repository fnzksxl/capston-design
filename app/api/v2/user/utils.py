from fastapi import HTTPException, status

from app.models import User


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
