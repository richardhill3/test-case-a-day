from .base_api import BaseAPI


class AuthAPI(BaseAPI):
    def __init__(self, base_url, session, username=None, password=None):
        super().__init__(base_url, session)
        self.username = username
        self.password = password

    def create_token(self, username=None, password=None):
        username = username or self.username
        password = password or self.password
        payload = {"username": username, "password": password}
        response = self._post("/auth", payload)
        response.raise_for_status()
        return response.json()["token"]

    def create(self, payload):
        return self._post("/auth", payload)
