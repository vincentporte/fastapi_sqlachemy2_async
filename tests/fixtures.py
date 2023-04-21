import pytest
from faker import Faker

from app.organizations.models import Organization
from app.services.database import sessionmanager

fake = Faker()


@pytest.fixture
async def organization():
    async with sessionmanager.session() as session:
        return await Organization.create(db=session, email=fake.email(), full_name=fake.name())


@pytest.fixture
async def organizations():
    async with sessionmanager.session() as session:
        await Organization.create(db=session, email=fake.email(), full_name=fake.name())
        await Organization.create(db=session, email=fake.email(), full_name=fake.name())
        return await Organization.get_all(db=session)
