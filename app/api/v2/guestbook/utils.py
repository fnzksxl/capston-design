from fastapi import HTTPException, status
from sqlalchemy import desc

from app.models import GuestBook


async def add_guestbook(data, id, db):
    try:
        row = GuestBook(message=data.message, owner_id=id, message_owner=data.message_owner)
        db.add(row)
        db.commit()

        return row
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{e} occured while adding guestbook",
        )


async def find_all_guestbook(db):
    return db.query(GuestBook).order_by(desc(GuestBook.created_at)).all()
