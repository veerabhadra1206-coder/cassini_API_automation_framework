import pytest

@pytest.mark.validation
class TestDataValidation:

    def test_missing_required_fields(self, clients, config):
        """TC_VALID_001: Missing Required Fields - GoRest"""
        headers = {"Authorization": f"Bearer {config['tokens']['gorest_token']}"}
        payload = {"name": "John Doe"}  # Missing required fields
        response, _ = clients["gorest"].post("/users", data=payload, headers=headers)
        data = response.json()

        # Validating status code
        assert response.status_code == 422
        assert isinstance(data, list)
        assert all("field" in err and "message" in err for err in data)

    def test_invalid_email_format(self, clients, config):
        """TC_VALID_002: Invalid Email Format - GoRest"""
        headers = {"Authorization": f"Bearer {config['tokens']['gorest_token']}"}
        payload = {
            "name": "John Doe",
            "email": "invalid-email-format",
            "gender": "male",
            "status": "active"
        }
        response, _ = clients["gorest"].post("/users", data=payload, headers=headers)
        data = response.json()

        # Validating status code
        assert response.status_code == 422
        assert any("email" in err["field"] for err in data)

    def test_invalid_enum_values(self, clients, config):
        """TC_VALID_003: Invalid Enum Values - GoRest"""
        headers = {"Authorization": f"Bearer {config['tokens']['gorest_token']}"}
        payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "gender": "unknown",
            "status": "maybe"
        }
        response, _ = clients["gorest"].post("/users", data=payload, headers=headers)
        data = response.json()

        # Validating status code
        assert response.status_code == 422
        fields = [err["field"] for err in data]
        assert "gender" in fields or "status" in fields
