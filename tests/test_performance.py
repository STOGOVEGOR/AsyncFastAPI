import time
from fastapi.testclient import TestClient
from api_async.main import app

client = TestClient(app)


def test_performance():
    start_time = time.time()
    response = client.get("/data")
    end_time = time.time()
    assert response.status_code == 200
    assert (end_time - start_time) < 3.0  # make sure the query runs faster than in 3 seconds
