from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("email, password, status_code",[
    ("kot@pes.com", "kotopes", 200),
    ("kot@pes.com", "kot0pes", 409),
    ("kot@pes.com", "kot0pes", 200),
    ("abcde", "pesokod", 422),
] )
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code",[
    ("test@test.com", "test", 200),
] )
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code