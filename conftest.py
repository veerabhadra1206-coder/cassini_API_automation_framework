import pytest
import yaml
import time
from utils.api_client import APIClient
from utils.logger import setup_logger


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    setup_logger()
# ------------------------------
# Config Fixture
# ------------------------------
@pytest.fixture(scope="session")
def config():
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)

# ------------------------------
# Clients Fixture
# ------------------------------
@pytest.fixture(scope="session")
def clients():
    return {
        "reqres": APIClient(
            base_url="https://reqres.in/api",
            api_key="reqres-free-v1",
        ),
        "jsonplaceholder": APIClient("https://jsonplaceholder.typicode.com"),
        "gorest": APIClient(
            "https://gorest.co.in/public/v2",
            api_key="a82d46266c9cd1757dbb39fd149d82eb63755482df9539a72e661518e838459e"
        ),
        "httpbin": APIClient("https://httpbin.org")
    }
# ------------------------------
# CRUD Data Management Fixtures
# ------------------------------
@pytest.fixture
def gorest_user(clients, config):
    headers = {"Authorization": f"Bearer {config['tokens']['gorest_token']}"}
    payload = {
        "name": "John Doe Automation",
        "email": f"john_{int(time.time())}@example.com",
        "gender": "male",
        "status": "active"
    }
    response, _ = clients["gorest"].post("/users", data=payload, headers=headers)
    user_data = response.json()
    user_id = user_data.get("id")
    yield user_data
    if user_id:
        clients["gorest"].delete(f"/users/{user_id}", headers=headers)

@pytest.fixture
def jsonplaceholder_post(clients):
    payload = {
        "title": "Temp Test Post",
        "body": "This is a temporary post for testing",
        "userId": 1
    }
    response, _ = clients["jsonplaceholder"].post("/posts", data=payload)
    post_data = response.json()
    post_id = post_data.get("id")
    yield post_data
    if post_id:
        clients["jsonplaceholder"].delete(f"/posts/{post_id}")
