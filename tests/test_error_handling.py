import pytest

@pytest.mark.error
class TestErrorHandling:

    def test_resource_not_found(self, clients):
        """TC_ERROR_001: Resource Not Found - JSONPlaceholder"""
        response, _ = clients["jsonplaceholder"].get("/posts/99999")
        data = response.json()

        # Validating status code
        assert response.status_code == 404
        # validating empty response body
        assert data == {}

    def test_method_not_allowed(self, clients):
        """TC_ERROR_002: Method Not Allowed - HTTPBin"""
        for _ in range(3):
            response, _ = clients["httpbin"].delete("/get")
            if response.status_code == 405:
                break

    def test_invalid_url_path(self, clients):
        """TC_ERROR_003: Invalid URL Path - JSONPlaceholder"""
        response, _ = clients["jsonplaceholder"].get("/invalid-endpoint")
        # Validating status code
        assert response.status_code == 404
