import pytest
from faker import Faker

from app.services.database import sessionmanager
from app.users.models import User

fake = Faker()


@pytest.fixture
async def user():
    async with sessionmanager.session() as session:
        return await User.create(db=session, email=fake.email(), full_name=fake.name())


@pytest.fixture
async def users():
    async with sessionmanager.session() as session:
        await User.create(db=session, email=fake.email(), full_name=fake.name())
        await User.create(db=session, email=fake.email(), full_name=fake.name())
        return await User.get_all(db=session)
