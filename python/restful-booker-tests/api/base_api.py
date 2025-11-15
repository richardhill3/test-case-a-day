import json


class BaseAPI:
    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    def _get(self, endpoint, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    def _post(self, endpoint, payload=None, **kwargs):
        return self.session.post(
            f"{self.base_url}{endpoint}", data=json.dumps(payload or {}), **kwargs
        )

    def _put(self, endpoint, payload=None, **kwargs):
        return self.session.put(
            f"{self.base_url}{endpoint}", data=json.dumps(payload or {}), **kwargs
        )

    def _patch(self, endpoint, payload=None, **kwargs):
        return self.session.patch(
            f"{self.base_url}{endpoint}", data=json.dumps(payload or {}), **kwargs
        )

    def _delete(self, endpoint, **kwargs):
        return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)
