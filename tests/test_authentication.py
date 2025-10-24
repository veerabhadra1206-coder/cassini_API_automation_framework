import pytest

@pytest.mark.auth
class TestAuthentication:
    def test_valid_login(self, clients):
        """TC_AUTH_001: Valid login should return token"""
        payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
        response, elapsed = clients["reqres"].post("/login", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert "token" in data, f"Token not found in response: {data}"
        assert isinstance(data["token"], str) and data["token"], "Token is empty or not a string"
        assert elapsed < 2, f"Response took too long: {elapsed:.2f} sec"

    def test_invalid_credentials(self, clients):
        """TC_AUTH_002: Invalid Credentials (ReqRes)"""
        payload = {"email": "eve.holt@reqres.in", "password": "wrongpassword"}
        response, _ = clients["reqres"].post("/login", json=payload)
        data = response.json()
        assert response.status_code == 400
        assert "error" in data
        assert "token" not in data

    def test_missing_password(self, clients):
        """TC_AUTH_003: Missing Password (ReqRes)"""
        payload = {"email": "eve.holt@reqres.in"}
        response, _ = clients["reqres"].post("/login", json=payload)
        data = response.json()

        # Validating status code
        assert response.status_code == 400
        assert data.get("error") == "Missing password"
