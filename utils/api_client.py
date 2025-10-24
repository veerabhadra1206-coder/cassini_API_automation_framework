import requests
import time
import logging

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url, timeout=10, api_key=None):
        self.base_url = base_url
        self.timeout = timeout
        self.api_key = api_key  # Store API key
        self._cleanup_queue = []

    # ------------------------------
    # Header preparation
    # ------------------------------
    def _prepare_headers(self, headers=None):
        headers = headers.copy() if headers else {}
        if self.api_key:
            headers['x-api-key'] = self.api_key
        return headers

    # ------------------------------
    # Logging helpers
    # ------------------------------
    def _log_request(self, method, url, headers=None, payload=None):
        logging.info(f"{method} {url}")


    def _log_response(self, response, elapsed):
        logging.info(f"{response.request.method} {response.url} | Status: {response.status_code} | Time: {elapsed:.2f}s")
        if response.status_code >= 400:
            logging.warning(f"Response body: {response.text}")


    # HTTP methods

    def get(self, endpoint, params=None, headers=None):
        headers = self._prepare_headers(headers)
        url = f"{self.base_url}{endpoint}"
        self._log_request("GET", url, headers=headers, payload=params)
        start_time = time.time()
        response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
        elapsed = time.time() - start_time
        self._log_response(response, elapsed)
        return response, elapsed

    def post(self, endpoint, data=None, json=None, headers=None):
        headers = self._prepare_headers(headers)
        url = f"{self.base_url}{endpoint}"
        self._log_request("POST", url, headers=headers, payload=json or data)
        start_time = time.time()
        response = requests.post(url, data=data, json=json, headers=headers, timeout=self.timeout)
        elapsed = time.time() - start_time
        self._log_response(response, elapsed)
        return response, elapsed

    def put(self, endpoint, data=None, json=None, headers=None):
        headers = self._prepare_headers(headers)
        url = f"{self.base_url}{endpoint}"
        self._log_request("PUT", url, headers=headers, payload=json or data)
        start_time = time.time()
        response = requests.put(url, data=data, json=json, headers=headers, timeout=self.timeout)
        elapsed = time.time() - start_time
        self._log_response(response, elapsed)
        return response, elapsed

    def delete(self, endpoint, headers=None):
        headers = self._prepare_headers(headers)
        url = f"{self.base_url}{endpoint}"
        self._log_request("DELETE", url, headers=headers)
        start_time = time.time()
        response = requests.delete(url, headers=headers, timeout=self.timeout)
        elapsed = time.time() - start_time
        self._log_response(response, elapsed)
        return response, elapsed
