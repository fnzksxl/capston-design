from ..user import utils
from .utils import add_tsitem, find_tsitems


async def addTsItem(data, cred, db):
    decoded_dict = await utils.verify_user(cred)
    row = await add_tsitem(data, decoded_dict.get("id"), db)

    return row


async def findTsItems(db):
    return await find_tsitems(db)
