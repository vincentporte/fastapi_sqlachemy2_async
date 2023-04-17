from typing import Mapping

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database import get_db
from app.services.exceptions import BadRequest, NotFound
from app.users.models import User as UserModel


async def valid_UUID4(user_id: str) -> str:
    try:
        return UUID4(user_id).hex
    except ValueError as exc:
        raise BadRequest() from exc


async def valid_user_id(user_id: str = Depends(valid_UUID4), db: AsyncSession = Depends(get_db)) -> Mapping:
    user = await UserModel.get(db, user_id)
    if not user:
        raise NotFound()
    return user


# TODO vincentporte : add a dependencies to manage duplicate email
