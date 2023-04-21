import uuid

import pytest
from faker import Faker
from sqlalchemy import select

from app.organizations.models import Organization
from app.services.database import sessionmanager
from tests.fixtures import organization, organizations  # noqa F401

fake = Faker()


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


@pytest.mark.asyncio
async def test_create_organization():
    async with sessionmanager.session() as session:
        email = fake.email()
        full_name = fake.name()
        created_organization = await Organization.create(db=session, email=email, full_name=full_name)

        # verify that the organization is added to the database
        result = await session.execute(select(Organization).filter_by(id=created_organization.id))
        assert result.scalar() == created_organization

        assert created_organization.email == email
        assert created_organization.full_name == full_name
        assert is_valid_uuid(created_organization.id)


@pytest.mark.asyncio
async def test_create_organization_with_id():
    async with sessionmanager.session() as session:
        email = fake.email()
        full_name = fake.name()
        id = fake.text(max_nb_chars=10)
        created_organization = await Organization.create(db=session, email=email, full_name=full_name, id=id)

        # verify that the organization is added to the database
        result = await session.execute(select(Organization).filter_by(id=created_organization.id))
        assert result.scalar() == created_organization

        assert created_organization.email == email
        assert created_organization.full_name == full_name
        assert created_organization.id == id


@pytest.mark.asyncio
async def test_create_organization_with_duplicated_email():
    async with sessionmanager.session() as session:
        email = fake.email()
        full_name = fake.name()
        created_organization = await Organization.create(db=session, email=email, full_name=full_name)

        created_organization = await Organization.create(db=session, email=email, full_name=full_name)
        assert created_organization is None


@pytest.mark.asyncio
async def test_get(organization):  # noqa F811
    async with sessionmanager.session() as session:
        result = await Organization.get(db=session, id=organization.id)
        assert result.email == organization.email
        assert result.full_name == organization.full_name


@pytest.mark.asyncio
async def test_get_with_invalid_id():
    async with sessionmanager.session() as session:
        result = await Organization.get(db=session, id="invalid_id")
        assert result is None


@pytest.mark.asyncio
async def test_get_all(organizations):  # noqa F811
    async with sessionmanager.session() as session:
        qs = await Organization.get_all(db=session)
        assert len(qs) == 2


@pytest.mark.asyncio
async def test_update(organization):  # noqa F811
    async with sessionmanager.session() as session:
        organization_to_update = await Organization.get(db=session, id=organization.id)
        email = fake.email()
        full_name = fake.name()

        updated_organization = await Organization.update(
            db=session, organization_data=organization_to_update, email=email, full_name=full_name
        )

        assert updated_organization.email == email
        assert updated_organization.full_name == full_name


@pytest.mark.asyncio
async def test_partial_update(organization):  # noqa F811
    async with sessionmanager.session() as session:
        organization_to_update = await Organization.get(db=session, id=organization.id)
        full_name = fake.name()

        updated_organization = await Organization.update(
            db=session, organization_data=organization_to_update, full_name=full_name
        )

        assert updated_organization.email == organization_to_update.email
        assert updated_organization.full_name == full_name


@pytest.mark.asyncio
async def test_update_with_duplicated_email(organizations):  # noqa F811
    async with sessionmanager.session() as session:
        organization_to_update = await Organization.get(db=session, id=organizations[0].id)

        updated_organization = await Organization.update(
            db=session, organization_data=organization_to_update, email=organizations[1].email
        )

        assert updated_organization is None


@pytest.mark.asyncio
async def test_delete(organization):  # noqa F811
    async with sessionmanager.session() as session:
        deleted_organization = await Organization.delete(db=session, organization=organization)

        assert deleted_organization == organization.email

        # verify that the organization is deleted from the database
        result = await session.execute(select(Organization).filter_by(id=organization.id))
        assert result.scalar() is None
