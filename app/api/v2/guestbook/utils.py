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


async def update_guestbook(message, id, owner_id, db):
    row = db.query(GuestBook).filter_by(id=id).first()
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Guestbook Not Found",
        )
    if row.owner_id == owner_id:
        row.message = message
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not owner")

    return row
