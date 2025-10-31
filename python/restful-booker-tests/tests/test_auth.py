from api.auth_api import AuthAPI


def test_create_token(auth_api: AuthAPI):
    token = auth_api.create_token()
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_token_invalid_creds(auth_api: AuthAPI):
    payload = {"username": "fakeUser", "password": "000111"}
    resp = auth_api.create(payload)
    assert resp.json()["reason"] == "Bad credentials"
    assert resp.status_code == 200
