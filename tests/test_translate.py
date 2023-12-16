import pytest
import json


@pytest.mark.asyncio
async def test_translate(client, token):
    body = {"dialect": "밥 뭇나?"}
    headers = {"Authorization": f"Bearer {token}"}
    r = await client.post("/AI", data=json.dumps(body), headers=headers)
    data = r.json()

    assert r.status_code == 200
    assert data.get("dialect") == body["dialect"]
