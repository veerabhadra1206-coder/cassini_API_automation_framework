import pytest
import time

@pytest.mark.crud
class TestCRUDOperations:

    def test_create_resource_jsonplaceholder(self, clients):
        """TC_CRUD_001: Create Resource - JSONPlaceholder"""
        payload = {
            "title": "Test Post Title",
            "body": "This is a test post body content for automation testing",
            "userId": 1
        }
        response, elapsed = clients["jsonplaceholder"].post("/posts", data=payload)
        data = response.json()

        # Validating status code
        assert response.status_code == 201
        assert "id" in data
        assert data["title"] == payload["title"]
        assert data["body"] == payload["body"]
        assert elapsed < 1

    def test_create_user_gorest(self, clients, config):
        """TC_CRUD_002: Create User - GoRest"""
        headers = {"Authorization": f"Bearer {config['tokens']['gorest_token']}"}
        payload = {
            "name": "John Doe Automation",
            "email": f"john_{int(time.time())}@example.com",  # ✅ unique
            "gender": "male",
            "status": "active"
        }
        response, _ = clients["gorest"].post("/users", data=payload, headers=headers)
        data = response.json()

        # Validating status code
        assert response.status_code == 201
        assert data["name"] == payload["name"]
        assert data["email"] == payload["email"]
        assert "id" in data

    def test_read_single_resource(self, clients):
        """TC_CRUD_003: Read Single Resource - JSONPlaceholder"""
        response, _ = clients["jsonplaceholder"].get("/posts/1")
        data = response.json()

        # Validating status code
        assert response.status_code == 200
        assert all(k in data for k in ["id", "title", "body", "userId"])
        assert isinstance(data["id"], int)
        assert isinstance(data["userId"], int)

