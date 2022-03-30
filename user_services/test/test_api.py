import pytest
from starlette.testclient import TestClient

from main import app


class TestApi:
    client: TestClient

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = TestClient(app)

    def test_ping(self):
        response = self.client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"message": "pong"}
