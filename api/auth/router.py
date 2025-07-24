from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
