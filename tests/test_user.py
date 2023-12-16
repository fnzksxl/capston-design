import pytest
import json


@pytest.mark.asyncio
async def test_add_user(client):
    body = {"email": "sample@sample.com", "password": "samplepw"}
    r = await client.post("/users/register", data=json.dumps(body))
    data = r.json()

    assert r.status_code == 201
    assert data.get("email") == body["email"]
