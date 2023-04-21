from typing import Mapping

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.organizations.models import Organization as OrganizationModel
from app.services.database import get_db
from app.services.exceptions import BadRequest, NotFound


async def valid_UUID4(organization_id: str) -> str:
    try:
        return UUID4(organization_id).hex
    except ValueError as exc:
        raise BadRequest() from exc


async def valid_organization_id(
    organization_id: str = Depends(valid_UUID4), db: AsyncSession = Depends(get_db)
) -> Mapping:
    organization = await OrganizationModel.get(db, organization_id)
    if not organization:
        raise NotFound()
    return organization


# TODO vincentporte : add a dependencies to manage duplicate email
