from typing import Dict, Mapping

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.organizations.dependencies import valid_organization_id
from app.organizations.models import Organization as OrganizationModel
from app.organizations.schemas import (
    OrganizationSchema,
    OrganizationSchemaCreate,
    OrganizationSchemaUpdate,
)
from app.services.database import get_db

router = APIRouter(prefix="/organizations")


@router.get("/{organization_id}/", response_model=OrganizationSchema)
async def get_organization(organization: Mapping = Depends(valid_organization_id)):
    return organization


# todo : add pagination
# todo : add authentification
@router.get("/", response_model=list[OrganizationSchema])
async def get_organizations(db: AsyncSession = Depends(get_db)):
    organizations = await OrganizationModel.get_all(db)
    return organizations


@router.post("/create/", response_model=OrganizationSchema)
async def create_organization(organization: OrganizationSchemaCreate, db: AsyncSession = Depends(get_db)):
    organization = await OrganizationModel.create(db, **organization.dict())
    if not organization:
        raise HTTPException(status_code=400, detail="Organization already exists")
    return organization


@router.patch("/{organization_id}/", response_model=OrganizationSchema)
async def update_organization(
    organization_datas: OrganizationSchemaUpdate,
    organization: OrganizationSchema = Depends(valid_organization_id),
    db: AsyncSession = Depends(get_db),
):
    updated_data = organization_datas.dict(exclude_unset=True)
    organization = await OrganizationModel.update(db, organization, **updated_data)
    if not organization:
        raise HTTPException(status_code=400, detail="Email already exists")
    return organization


@router.delete("/{organization_id}/", response_model=Dict[str, str])
async def delete_organization(organization: dict = Depends(valid_organization_id), db: AsyncSession = Depends(get_db)):
    res = await OrganizationModel.delete(organization, db)
    return {"message": f"Organization {res} deleted successfully"}
