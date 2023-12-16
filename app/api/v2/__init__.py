from fastapi import APIRouter

from .user import controller as user
from .translate import controller as translate
from .item import controller as item

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["UserV2"])
router.include_router(translate.router, prefix="/AI", tags=["AIV2"])
router.include_router(item.router, prefix="/items", tags=["ItemV2"])
