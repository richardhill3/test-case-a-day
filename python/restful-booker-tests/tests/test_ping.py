from api.healthcheck_api import HealthCheckAPI


def test_ping(healthcheck_api: HealthCheckAPI):
    ping_resp = healthcheck_api.get()
    assert ping_resp.ok
    assert ping_resp.status_code == 201
