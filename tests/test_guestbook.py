import pytest
import json


@pytest.mark.asyncio
async def test_add_guestbook(client, token):
    body = {"message": "test", "message_owner": "testowner"}
    headers = {"Authorization": f"Bearer {token}"}

    r = await client.post("/guestbooks", data=json.dumps(body), headers=headers)
    data = r.json()

    assert r.status_code == 201
    assert data.get("message") == body["message"]


@pytest.mark.asyncio
async def test_add_guestbook_failed_by_long_owner(client, token):
    body = {"message": "test", "message_owner": "a" * 25}
    headers = {"Authorization": f"Bearer {token}"}

    r = await client.post("/guestbooks", data=json.dumps(body), headers=headers)

    assert r.status_code == 422


@pytest.mark.asyncio
async def test_get_guestbooks(client, guestbook):
    r = await client.get("/guestbooks")
    data = r.json()

    assert r.status_code == 200
    assert data[0].get("id") == guestbook.id
