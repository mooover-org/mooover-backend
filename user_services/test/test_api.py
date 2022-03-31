import http.client

import pytest
from starlette.testclient import TestClient

from main import app


class TestApi:
    client: TestClient
    access_token: str
    user1: dict
    user2: dict

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = TestClient(app)
        conn = http.client.HTTPSConnection("dev-ed4pmqgq.eu.auth0.com")
        payload = "{\"client_id\":\"V6ZVwOyzvgxrhqiZJeb1RHGypfVORq3T\"," \
                  "\"client_secret\":\"2eOAvMzqd1BX7QF9D" \
                  "-Fl6iom1B8pbXFvJVX7uMPp9PDTkL2_wBrmFLGh3ojlivCc\"," \
                  "\"audience\":\"mooover/api\",\"grant_type\":\"client_credentials\"} "
        headers = {'content-type': "application/json"}
        conn.request("POST", "/oauth/token", payload, headers)
        res = conn.getresponse()
        data = res.read()
        self.access_token = data.decode("utf-8").split("\"")[3]
        self.user1 = {"id": "1", "name": "test", "given_name": "test",
                      "family_name": "test", "nickname": "test",
                      "email": "test@test.test", "picture": "test"}
        self.user2 = {"id": "2", "name": "test", "given_name": "test",
                      "family_name": "test", "nickname": "test",
                      "email": "test@test.test", "picture": "test"}

    def test_ping(self):
        response = self.client.get("/api/v1/users/ping")
        assert response.status_code == 200
        assert response.json() == "pong"

    def test_get_user(self):
        self.client.post(
            "/api/v1/users",
            json=self.user1,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        response = self.client.get(
            "/api/v1/users/1",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 200
        assert response.json() == self.user1
        response = self.client.get(
            "/api/v1/users/-1",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 404

    def test_add_user(self):
        response = self.client.post(
            "/api/v1/users",
            json=self.user2,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 201
        assert response.json() == self.user2
        response = self.client.post(
            "/api/v1/users",
            json=self.user2,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        assert response.status_code == 409
