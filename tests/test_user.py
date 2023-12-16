import pytest
import json


@pytest.mark.asyncio
async def test_add_user(client):
    body = {"email": "sample@sample.com", "password": "samplepw"}
    r = await client.post("/users/register", data=json.dumps(body))
    data = r.json()

    assert r.status_code == 201
    assert data.get("email") == body["email"]


@pytest.mark.asyncio
async def test_email_duplicated_exist(client, user):
    body = {"email": "test@sample.com"}
    r = await client.post("/users/duplicated", data=json.dumps(body))
    data = r.json()

    assert r.status_code == 200
    assert data.get("duplicated")
    assert body["email"] == user.email


@pytest.mark.asyncio
async def test_email_duplicated_no_exist(client):
    body = {"email": "notexist@sample.com"}
    r = await client.post("/users/duplicated", data=json.dumps(body))
    data = r.json()

    assert r.status_code == 200
    assert not data.get("duplicated")
