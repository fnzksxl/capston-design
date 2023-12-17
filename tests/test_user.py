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
async def test_add_user_failed_by_long_email(client):
    body = {"email": "longlonglonglonglonglonglonglonglongmail@sample.com", "password": "samplepw"}
    r = await client.post("/users/register", data=json.dumps(body))

    assert r.status_code == 422


@pytest.mark.asyncio
async def test_email_duplicated_exist(client, user):
    email = "test@sample.com"
    r = await client.get(f"/users/duplicated?email={email}")
    data = r.json()

    assert r.status_code == 200
    assert data.get("duplicated")
    assert email == user.email


@pytest.mark.asyncio
async def test_email_duplicated_no_exist(client):
    email = "noexist@sample.com"
    r = await client.get(f"/users/duplicated?email={email}")
    data = r.json()

    assert r.status_code == 200
    assert not data.get("duplicated")


@pytest.mark.asyncio
async def test_login_user(client, user):
    body = {"email": user.email, "password": "testpw"}
    r = await client.post("/users/login", data=json.dumps(body))
    data = r.json()

    assert r.status_code == 200
    assert data.get("user_id") == user.id


@pytest.mark.asyncio
async def test_login_user_invalid_pw(client, user):
    body = {"email": user.email, "password": "wrongpw"}
    r = await client.post("/users/login", data=json.dumps(body))
    data = r.json()

    assert r.status_code == 403
    assert data.get("detail") == "Incorrect Password"


@pytest.mark.asyncio
async def test_login_user_invalid_email(client):
    body = {"email": "noemail", "password": "testpw"}
    r = await client.post("/users/login", data=json.dumps(body))
    data = r.json()

    assert r.status_code == 403
    assert data.get("detail") == "No Email Found"
