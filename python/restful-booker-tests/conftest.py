import pytest
import requests
from api.auth_api import AuthAPI
from api.booking_api import BookingAPI
from api.healthcheck_api import HealthCheckAPI

BASE_URL = "http://localhost:3001"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def session():
    session = requests.Session()
    session.headers.update({"Content-type": "application/json"})
    return session


@pytest.fixture(scope="session")
def auth_api(base_url, session):
    return AuthAPI(base_url, session)


@pytest.fixture(scope="session")
def booking_api(base_url, session):
    return BookingAPI(base_url, session)


@pytest.fixture(scope="session")
def healthcheck_api(base_url, session):
    return HealthCheckAPI(base_url, session)
