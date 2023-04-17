import uuid

import pytest
from faker import Faker
from sqlalchemy import select

from app.services.database import sessionmanager
from app.users.models import User
from tests.fixtures import user, users  # noqa F401

fake = Faker()


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


@pytest.mark.asyncio
async def test_create_user():
    async with sessionmanager.session() as session:
        email = fake.email()
        full_name = fake.name()
        created_user = await User.create(db=session, email=email, full_name=full_name)

        # verify that the user is added to the database
        result = await session.execute(select(User).filter_by(id=created_user.id))
        assert result.scalar() == created_user

        assert created_user.email == email
        assert created_user.full_name == full_name
        assert is_valid_uuid(created_user.id)


@pytest.mark.asyncio
async def test_create_user_with_id():
    async with sessionmanager.session() as session:
        email = fake.email()
        full_name = fake.name()
        id = fake.text(max_nb_chars=10)
        created_user = await User.create(db=session, email=email, full_name=full_name, id=id)

        # verify that the user is added to the database
        result = await session.execute(select(User).filter_by(id=created_user.id))
        assert result.scalar() == created_user

        assert created_user.email == email
        assert created_user.full_name == full_name
        assert created_user.id == id


@pytest.mark.asyncio
async def test_create_user_with_duplicated_email():
    async with sessionmanager.session() as session:
        email = fake.email()
        full_name = fake.name()
        created_user = await User.create(db=session, email=email, full_name=full_name)

        created_user = await User.create(db=session, email=email, full_name=full_name)
        assert created_user is None


@pytest.mark.asyncio
async def test_get(user):  # noqa F811
    async with sessionmanager.session() as session:
        result = await User.get(db=session, id=user.id)
        assert result.email == user.email
        assert result.full_name == user.full_name


@pytest.mark.asyncio
async def test_get_with_invalid_id():
    async with sessionmanager.session() as session:
        result = await User.get(db=session, id="invalid_id")
        assert result is None


@pytest.mark.asyncio
async def test_get_all(users):  # noqa F811
    async with sessionmanager.session() as session:
        qs = await User.get_all(db=session)
        assert len(qs) == 2
