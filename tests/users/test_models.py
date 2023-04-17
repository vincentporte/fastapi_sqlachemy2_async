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


@pytest.mark.asyncio
async def test_update(user):  # noqa F811
    async with sessionmanager.session() as session:
        user_to_update = await User.get(db=session, id=user.id)
        email = fake.email()
        full_name = fake.name()

        updated_user = await User.update(db=session, user_data=user_to_update, email=email, full_name=full_name)

        assert updated_user.email == email
        assert updated_user.full_name == full_name


@pytest.mark.asyncio
async def test_partial_update(user):  # noqa F811
    async with sessionmanager.session() as session:
        user_to_update = await User.get(db=session, id=user.id)
        full_name = fake.name()

        updated_user = await User.update(db=session, user_data=user_to_update, full_name=full_name)

        assert updated_user.email == user_to_update.email
        assert updated_user.full_name == full_name


@pytest.mark.asyncio
async def test_update_with_duplicated_email(users):  # noqa F811
    async with sessionmanager.session() as session:
        user_to_update = await User.get(db=session, id=users[0].id)

        updated_user = await User.update(db=session, user_data=user_to_update, email=users[1].email)

        assert updated_user is None


@pytest.mark.asyncio
async def test_delete(user):  # noqa F811
    async with sessionmanager.session() as session:
        deleted_user = await User.delete(db=session, user=user)

        assert deleted_user == user.email

        # verify that the user is deleted from the database
        result = await session.execute(select(User).filter_by(id=user.id))
        assert result.scalar() is None
