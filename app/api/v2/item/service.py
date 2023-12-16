from ..user import utils
from .utils import add_tsitem, find_tsitems, delete_tsitem


async def addTsItem(data, cred, db):
    decoded_dict = await utils.verify_user(cred)
    row = await add_tsitem(data, decoded_dict.get("id"), db)

    return row


async def findTsItems(db):
    return await find_tsitems(db)


async def deleteTsItem(data, cred, db):
    if await utils.verify_user(cred):
        return await delete_tsitem(data.id, db)
