from .base_api import BaseAPI


class AuthAPI(BaseAPI):
    def create_token(self, username="admin", password="password123"):
        payload = {"username": username, "password": password}
        response = self._post("/auth", payload)
        response.raise_for_status()
        return response.json()["token"]
