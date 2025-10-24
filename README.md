# Cassini API Automation Framework

## Description
Pytest + Requests based API Automation Framework built for Cassini Technical Assessment.

## Structure
- `config/config.yaml` : Contains base URLs and tokens
- `utils/api_client.py` : Handles HTTP requests and logging
- `conftest.py` : Initializes clients and loads configuration
- `tests/test_authentication.py` : Authentication API tests (ReqRes)
- `reports/` : HTML reports after execution

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run tests with HTML report:
   ```bash
   pytest -v --html=reports/report.html --self-contained-html
   ```
