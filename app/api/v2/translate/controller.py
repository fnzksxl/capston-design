from fastapi import Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .schema import Translated, ToTranslate
from .service import itemTranslate

router = APIRouter()
security = HTTPBearer()


@router.post("", response_model=Translated)
async def translate_item(
    data: ToTranslate,
    cred: HTTPAuthorizationCredentials = Depends(security),
):
    return await itemTranslate(data, cred)
