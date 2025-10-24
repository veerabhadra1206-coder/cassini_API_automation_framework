import pytest

@pytest.mark.edge
class TestEdgeCases:

    def test_empty_request_body(self, clients, config):
        """TC_EDGE_001: Empty Request Body - GoRest"""
        headers = {"Authorization": f"Bearer {config['tokens']['gorest_token']}"}
        response, _ = clients["gorest"].post("/users", data={}, headers=headers)
        data = response.json()

        # Validating status code
        assert response.status_code in [400, 422]
        assert isinstance(data, list) or isinstance(data, dict)

    def test_maximum_string_lengths(self, clients, config):
        """TC_EDGE_002: Maximum String Lengths"""
        headers = {"Authorization": f"Bearer {config['tokens']['gorest_token']}"}
        payload = {
            "name": "A" * 250,
            "email": f"{'b'*50}@example.com",
            "gender": "male",
            "status": "active"
        }
        response, _ = clients["gorest"].post("/users", data=payload, headers=headers)
        # Validating status code
        assert response.status_code in [201, 422]

    def test_unicode_special_characters(self, clients, config):
        """TC_EDGE_003: Unicode and Special Characters"""
        headers = {"Authorization": f"Bearer {config['tokens']['gorest_token']}"}
        payload = {
            "name": "José María González-Pérez £$%^",
            "email": "jose.muller@example.com",
            "gender": "male",
            "status": "active"
        }
        response, _ = clients["gorest"].post("/users", data=payload, headers=headers)
        # Validating status code
        assert response.status_code in [201, 422]
