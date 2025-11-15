"""
Health Check Tests for Restful-Booker API

Tests from Section 2.7 of the test plan covering API health check endpoints.
Test names include the test ID as per requirements (e.g., test_HEALTH_001_ping_response_status)
"""

from api.healthcheck_api import HealthCheckAPI


class TestHealthCheck:
    """Health check tests verifying API availability and status endpoints"""

    def test_HEALTH_001_ping_response_status(self, healthcheck_api: HealthCheckAPI):
        """
        HEALTH-001: Ping Response Status
        GET /ping and verify HTTP 201 status code is returned with ok response
        Expected: Returns HTTP 201 Created
        """
        ping_resp = healthcheck_api.get()
        assert ping_resp.status_code == 201
        assert ping_resp.ok

    def test_HEALTH_002_ping_response_body(self, healthcheck_api: HealthCheckAPI):
        """
        HEALTH-002: Ping Response Body
        GET /ping and verify response body contains success message
        Expected: HTTP 201 with message body ("Created" or "OK")
        """
        ping_resp = healthcheck_api.get()
        assert ping_resp.status_code == 201
        # Verify response body contains success message
        assert ping_resp.text.strip() in ["Created", "OK"] or "OK" in ping_resp.text
