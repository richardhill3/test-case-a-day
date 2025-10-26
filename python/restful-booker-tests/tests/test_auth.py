from api.auth_api import AuthAPI


def test_create_token(auth_api: AuthAPI):
    token = auth_api.create_token()
    assert isinstance(token, str)
    assert len(token) > 0
