from fastapi import APIRouter

from . import user, item, translate, guestbook

router = APIRouter()
router.include_router(user.router, prefix='/users', tags=["User"])
router.include_router(item.router, prefix='/items', tags=["TsItem"])
router.include_router(translate.router, prefix='/translate', tags=["AI"])
router.include_router(guestbook.router, prefix='/guestbook', tags=["GuestBook"])