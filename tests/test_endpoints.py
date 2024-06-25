import pytest
from fastapi.testclient import TestClient
from api_async.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_data():
    response = client.get("/data")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "id" in data[0]
        assert "name" in data[0]
