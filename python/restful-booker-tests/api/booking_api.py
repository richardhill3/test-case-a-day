from .base_api import BaseAPI


class BookingAPI(BaseAPI):
    def get_all(self):
        return self._get("/booking")

    def get(self, booking_id):
        return self._get(f"/booking/{booking_id}")

    def create(self, payload):
        return self._post("/booking", payload)

    def update(self, booking_id, payload, token):
        headers = {"Cookie": f"token={token}"}
        return self._put(f"/booking/{booking_id}", payload, headers=headers)

    def delete(self, booking_id, token):
        headers = {"Cookie": f"token={token}"}
        return self._delete(f"/booking/{booking_id}", headers=headers)
