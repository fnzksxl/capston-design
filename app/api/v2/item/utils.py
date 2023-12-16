from fastapi import HTTPException, status

from app.models import TsItem


async def add_tsitem(data, id, db):
    try:
        row = TsItem(**data.dict(), owner_id=id)
        db.add(row)
        db.commit()

        return row
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{e} occured while adding tsitem",
        )


async def find_tsitems(db):
    row = db.query(TsItem).all()

    return row


async def delete_tsitem(id, db):
    try:
        row = db.query(TsItem).filter_by(id=id).first()
        db.delete(row)
        db.commit()

        return row
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Item Found",
        )
