# Python testing of a REST Api

[![Python Restful-Booker API Tests](https://github.com/richardhill3/test-case-a-day/actions/workflows/rb-python-api-tests.yaml/badge.svg)](https://github.com/richardhill3/test-case-a-day/actions/workflows/rb-python-api-tests.yaml)

## 1. Overview

Test project in Python using `pytest` and `requests` package to demonstrate functional testing of an REST Api using Restful-booker demo applications

## 2. Key Interest Points for learning

* While not required for a simple API, the test project has been developed with a service object model to demonstrate the pattern often used with frameworks like Selninum and Playwright and the Page Object Model can also be utilized for API services.
* `conftest.py` is being utilized to provide common objects to all tests, ex: `Base_url`, `requests.Session`, and clients for each api endpoint / service for the system under test.
* GitHub Actions workflow available at `/.github/workflows/rb-python-api-tests.yaml` perform these steps:
  * Pulls main repo
  * `/sut/restful-booker/docker-compose.yml` will standup the application for testing and ensure it is available
  * Syncs requirements through UV
  * Executes pytest with HTML report output
  * Uploads HTML test report as artifact of workflow
* Project dependencies and virtual environment managed with UV.


## 4. References

* [Restful Booker API Documentation](https://restful-booker.herokuapp.com/apidoc/index.html)
* [Pytest Documentation](https://docs.pytest.org/)
* [Requests Library](https://requests.readthedocs.io/)
* [Docker Compose Reference](https://docs.docker.com/compose/)