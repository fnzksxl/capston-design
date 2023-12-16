from ..user import utils
from .utils import add_guestbook


async def addGuestBook(data, cred, db):
    decoded_dict = await utils.verify_user(cred)
    return await add_guestbook(data, decoded_dict.get("id"), db)
