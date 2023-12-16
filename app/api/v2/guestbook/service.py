from ..user import utils
from .utils import add_guestbook, find_all_guestbook


async def addGuestBook(data, cred, db):
    decoded_dict = await utils.verify_user(cred)
    return await add_guestbook(data, decoded_dict.get("id"), db)


async def findAllGuestBook(db):
    return await find_all_guestbook(db)
