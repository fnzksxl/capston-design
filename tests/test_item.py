import pytest
import json


@pytest.mark.asyncio
async def test_add_item(client, token):
    body = {
        "dialect": "dialect",
        "standard": "standard",
        "english": "english",
        "chinese": "chinese",
        "japanese": "japanese",
    }
    headers = {"Authorization": f"Bearer {token}"}

    r = await client.post("/items", data=json.dumps(body), headers=headers)
    data = r.json()

    assert r.status_code == 201
    assert data.get("dialect") == body["dialect"]
    assert data.get("standard") == body["standard"]
    assert data.get("english") == body["english"]
    assert data.get("chinese") == body["chinese"]
    assert data.get("japanese") == body["japanese"]


@pytest.mark.asyncio
async def test_add_item_failed_by_long_text(client, token):
    body = {
        "dialect": "a" * 256,
        "standard": "standard",
        "english": "english",
        "chinese": "chinese",
        "japanese": "japanese",
    }
    headers = {"Authorization": f"Bearer {token}"}

    r = await client.post("/items", data=json.dumps(body), headers=headers)

    assert r.status_code == 422
