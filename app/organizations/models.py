from uuid import uuid4

from sqlalchemy import Column, String, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.organizations.schemas import OrganizationSchema
from app.services.database import Base


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)

    @classmethod
    async def create(cls, db: AsyncSession, id=None, **kwargs):
        if not id:
            id = uuid4().hex

        transaction = cls(id=id, **kwargs)
        db.add(transaction)
        try:
            await db.commit()
            await db.refresh(transaction)
        except IntegrityError:
            await db.rollback()
            return None
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, id: str):
        try:
            transaction = await db.get(cls, id)
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(cls, db: AsyncSession):
        return (await db.execute(select(cls))).scalars().all()

    @classmethod
    async def update(cls, db: AsyncSession, organization_data: OrganizationSchema, **kwargs):
        for key, value in kwargs.items():
            setattr(organization_data, key, value) if value else None
        try:
            await db.commit()
            await db.refresh(organization_data)
        except IntegrityError:
            await db.rollback()
            return None
        return organization_data

    @classmethod
    async def delete(cls, organization, db: AsyncSession):
        await db.delete(organization)
        await db.commit()
        return organization.email
