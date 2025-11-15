"""
Authentication Tests for Restful-Booker API

Tests from Section 2.1 of the test plan covering authentication mechanisms.
Test names include the test ID as per requirements (e.g., test_AUTH_001_valid_credentials)
"""

from api.auth_api import AuthAPI


class TestAuthentication:
    """Authentication tests covering token creation and credential validation"""

    def test_AUTH_001_valid_credentials(self, auth_api: AuthAPI):
        """
        AUTH-001: Valid Credentials
        POST /auth with valid username (admin) and password (password123)
        Expected: Returns token string
        """
        token = auth_api.create_token()
        assert isinstance(token, str)
        assert len(token) > 0

    def test_AUTH_002_invalid_username(self, auth_api: AuthAPI):
        """
        AUTH-002: Invalid Username
        POST /auth with incorrect username
        Expected: Returns HTTP 200 with "Bad credentials"
        """
        payload = {"username": "invalidUser", "password": "password123"}
        resp = auth_api.create(payload)
        assert resp.json()["reason"] == "Bad credentials"
        assert resp.status_code == 200

    def test_AUTH_003_invalid_password(self, auth_api: AuthAPI):
        """
        AUTH-003: Invalid Password
        POST /auth with incorrect password
        Expected: Returns HTTP 200 with "Bad credentials"
        """
        payload = {"username": "fakeUser", "password": "000111"}
        resp = auth_api.create(payload)
        assert resp.json()["reason"] == "Bad credentials"
        assert resp.status_code == 200

    def test_AUTH_004_missing_username(self, auth_api: AuthAPI):
        """
        AUTH-004: Missing Username
        POST /auth without username field
        Expected: Returns HTTP 200 with "Bad credentials"
        """
        payload = {"password": "password123"}
        resp = auth_api.create(payload)
        assert resp.status_code == 200
        assert resp.json()["reason"] == "Bad credentials"

    def test_AUTH_005_missing_password(self, auth_api: AuthAPI):
        """
        AUTH-005: Missing Password
        POST /auth without password field
        Expected: Returns HTTP 200 with "Bad credentials"
        """
        payload = {"username": "admin"}
        resp = auth_api.create(payload)
        assert resp.status_code == 200
        assert resp.json()["reason"] == "Bad credentials"

    def test_AUTH_006_empty_credentials(self, auth_api: AuthAPI):
        """
        AUTH-006: Empty Credentials
        POST /auth with empty username and password
        Expected: Returns HTTP 200 with "Bad credentials"
        """
        payload = {"username": "", "password": ""}
        resp = auth_api.create(payload)
        assert resp.status_code == 200
        assert resp.json()["reason"] == "Bad credentials"

    def test_AUTH_007_token_persistence(self, auth_api: AuthAPI, booking_api):
        """
        AUTH-007: Token Persistence
        Verify token can be used in subsequent requests
        Expected: Token should work for protected endpoints
        """
        token = auth_api.create_token()
        assert isinstance(token, str)
        assert len(token) > 0

        resp = booking_api.delete(1, token=token)
        assert resp.status_code != 401
