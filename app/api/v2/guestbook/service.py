from ..user import utils
from .utils import add_guestbook, find_all_guestbook, update_guestbook


async def addGuestBook(data, cred, db):
    decoded_dict = await utils.verify_user(cred)
    return await add_guestbook(data, decoded_dict.get("id"), db)


async def findAllGuestBook(db):
    return await find_all_guestbook(db)


async def updateGuestBook(data, cred, db):
    decoded_dict = await utils.verify_user(cred)
    return await update_guestbook(data.message, data.id, decoded_dict.get("id"), db)
