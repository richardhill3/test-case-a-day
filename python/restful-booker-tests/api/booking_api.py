from .base_api import BaseAPI


class BookingAPI(BaseAPI):
    def get_all(self, firstname=None, lastname=None, checkin=None, checkout=None):
        params = {}
        if firstname:
            params["firstname"] = firstname
        if lastname:
            params["lastname"] = lastname
        if checkin:
            params["checkin"] = checkin
        if checkout:
            params["checkout"] = checkout
        return self._get("/booking", params=params)

    def get(self, booking_id):
        return self._get(f"/booking/{booking_id}")

    def create(self, payload):
        return self._post("/booking", payload)

    def update(self, booking_id, payload, token):
        headers = {"Cookie": f"token={token}"}
        return self._put(f"/booking/{booking_id}", payload, headers=headers)

    def partial_update(self, booking_id, payload, token):
        headers = {"Cookie": f"token={token}"}
        return self._patch(f"/booking/{booking_id}", payload, headers=headers)

    def delete(self, booking_id, token):
        headers = {"Cookie": f"token={token}"}
        return self._delete(f"/booking/{booking_id}", headers=headers)
