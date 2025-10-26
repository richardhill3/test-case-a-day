from .base_api import BaseAPI


class HealthCheckAPI(BaseAPI):
    def get(self):
        return self._get("/ping")
