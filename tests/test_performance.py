import pytest
import concurrent.futures
import time
import requests
import logging

@pytest.mark.performance
class TestPerformance:

    def test_response_time_validation(self, clients):
        """TC_PERF_001: Response Time Validation - JSONPlaceholder"""
        endpoints = ["/posts", "/posts/1"]
        for ep in endpoints:
            response, elapsed = clients["jsonplaceholder"].get(ep)
            assert response.status_code == 200
            assert elapsed < 2

    def test_concurrent_request_handling(self, clients):
        """TC_PERF_002: Concurrent Request Handling - HTTPBin"""
        endpoint = "/delay/1"
        num_requests = 10
        max_workers = 10
        results = []

        start_time = time.time()

        # Function with retry for timeout
        def safe_get(ep, retries=1):
            try:
                resp, _ = clients["httpbin"].get(ep)
                return resp
            except requests.exceptions.ReadTimeout:
                if retries > 0:
                    time.sleep(0.5)
                    return safe_get(ep, retries=retries - 1)
                return None

        # Run concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(safe_get, endpoint) for _ in range(num_requests)]
            results = [f.result() for f in futures]

        total_time = time.time() - start_time

        # Validate all requests succeeded
        assert all(r and r.status_code == 200 for r in results), "Some requests failed"

        # Validate total time (roughly 1s per request ideally, allow buffer)
        assert total_time < 12, f"Total concurrent execution too long: {total_time:.2f}s"

        # Optional: log average response time for monitoring
        response_times = [r.elapsed.total_seconds() for r in results if r]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            logging.info(f"Average concurrent response time: {avg_response_time:.2f}s")

    def test_pagination_performance(self, clients):
        """TC_PERF_003: Pagination Performance - JSONPlaceholder"""
        for page in range(1, 4):
            response, elapsed = clients["jsonplaceholder"].get(f"/posts?_page={page}&_limit=20")
            assert response.status_code == 200
            assert elapsed < 1.5

    def test_stress_test(self, clients):
        """TC_PERF_004: Stress Test - HTTPBin Echo"""
        endpoint = "/post"
        payload = {"data": "x" * 1024}  # 1KB payload
        num_requests = 50
        max_workers = 10
        results = []

        start_time = time.time()

        # Function with retry for timeout
        def safe_post(ep, data, retries=1):
            try:
                resp, _ = clients["httpbin"].post(ep, json=data)
                return resp
            except requests.exceptions.ReadTimeout:
                if retries > 0:
                    time.sleep(0.5)  # small backoff
                    return safe_post(ep, data, retries=retries-1)
                else:
                    return None

        # Run concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(safe_post, endpoint, payload) for _ in range(num_requests)]
            results = [f.result() for f in futures]

        total_time = time.time() - start_time

        # Validate success rate
        success_count = sum(1 for r in results if r and r.status_code == 200)
        success_rate = success_count / num_requests
        assert success_rate >= 0.95, f"Success rate too low: {success_rate:.2%}"

        # Validate total execution time (approximate)
        assert total_time <= 30, f"Stress test took too long: {total_time:.2f}s"

        # Optional: average response time
        response_times = [r.elapsed.total_seconds() for r in results if r]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            logging.info(f"Average response time: {avg_response_time:.2f}s")