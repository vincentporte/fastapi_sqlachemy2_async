import pytest
from faker import Faker

from app.organizations.dependencies import valid_organization_id, valid_UUID4
from app.services.database import sessionmanager
from app.services.exceptions import BadRequest, NotFound
from tests.fixtures import organization  # noqa: F401

fake = Faker()


@pytest.mark.asyncio
async def test_valid_UUID4():
    uuid = fake.uuid4()
    result = await valid_UUID4(uuid)
    assert result == uuid.replace("-", "")


@pytest.mark.asyncio
async def test_valid_uuid4_with_invalid_uuid4():
    with pytest.raises(BadRequest) as exc_info:
        await valid_UUID4("invalid_uuid")
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_valid_organization_id(organization):  # noqa: F811
    async with sessionmanager.session() as session:
        result = await valid_organization_id(organization_id=organization.id, db=session)
        assert result.id == organization.id


@pytest.mark.asyncio
async def test_valid_organization_id_with_unexistent_uuid():
    async with sessionmanager.session() as session:
        with pytest.raises(NotFound) as exc_info:
            await valid_organization_id(organization_id=fake.uuid4(), db=session)
        assert exc_info.value.status_code == 404
