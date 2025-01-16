import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.factories import AplicationFactory


@pytest.mark.asyncio
async def test_create_aplication(test_client: AsyncClient):
    response = await test_client.post(
        "/aplications",
        json={"user_name": "testuser", "description": "test_desc"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_name"] == "testuser"


@pytest.mark.asyncio
async def test_read_aplication(test_client: AsyncClient, session: AsyncSession):
    AplicationFactory._meta.sqlalchemy_session = session
    aplications = [AplicationFactory(), AplicationFactory(), AplicationFactory()]
    for aplication in aplications:
        session.add(aplication)
        await session.commit()

    response = await test_client.get("/aplications")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
