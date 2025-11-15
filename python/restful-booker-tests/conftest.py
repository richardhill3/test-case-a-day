import pytest
import os
import requests
from dotenv import load_dotenv
from api.auth_api import AuthAPI
from api.booking_api import BookingAPI
from api.healthcheck_api import HealthCheckAPI

# Load environment variables from .env file
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:3001")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def auth_username():
    return os.getenv("AUTH_USERNAME")


@pytest.fixture(scope="session")
def auth_password():
    return os.getenv("AUTH_PASSWORD")


@pytest.fixture(scope="session")
def session():
    session = requests.Session()
    session.headers.update({"Content-type": "application/json"})
    return session


@pytest.fixture(scope="session")
def auth_api(base_url, session, auth_username, auth_password):
    return AuthAPI(base_url, session, username=auth_username, password=auth_password)


@pytest.fixture(scope="session")
def booking_api(base_url, session):
    return BookingAPI(base_url, session)


@pytest.fixture(scope="session")
def healthcheck_api(base_url, session):
    return HealthCheckAPI(base_url, session)
