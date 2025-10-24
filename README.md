# Cassini API Automation Framework

## Description
Pytest + Requests based API Automation Framework built for Cassini Technical Assessment.

## Structure
- `config/config.yaml` : Contains base URLs and tokens
- `utils/api_client.py` : Handles HTTP requests and logging
- `conftest.py` : Initializes clients and loads configuration
- `tests/` : API tests 
- `reports/` : HTML reports after execution
- `utils/logger.py`: All requests and responses are logged to `logs/test_run.log`.
                  Old logs are cleared automatically at the start of each test run

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run tests with HTML report:
   ```bash
   pytest -v --html=reports/report.html --self-contained-html
   ```
## CI/CD Integration

- GitHub Actions workflow is included in `.github/workflows/api_automation.yml`

### Workflow Triggers
- Push to `main` branch
- Pull requests to `main` branch

### Workflow Steps
1. Checkout Repository
2. Setup Python
3. Install Dependencies
4. Create Reports Folder 
5. Run API Tests and Generate HTML Report
6. Upload HTML Report as an Artifact
