from utils import sample_booking


def test_booking_crud_flow(booking_api, auth_api):
    # 1. Create Booking
    payload = sample_booking("Alice", "Smith")
    create_resp = booking_api.create(payload)
    assert create_resp.status_code == 200

    data = create_resp.json()
    booking_id = data["bookingid"]

    # 2. Retrieve Booking
    get_resp = booking_api.get(booking_id)
    assert get_resp.status_code == 200
    assert get_resp.json()["firstname"] == "Alice"

    # 3. Update Booking
    token = auth_api.create_token()
    updated_payload = {**payload, "firstname": "Updated"}
    update_resp = booking_api.update(booking_id, updated_payload, token)
    assert update_resp.status_code == 200
    assert update_resp.json()["firstname"] == "Updated"

    # 4. Delete Booking
    delete_resp = booking_api.delete(booking_id, token)
    assert delete_resp.status_code == 201

    # 5. Confirm Deletion (should return 404)
    confirm_resp = booking_api.get(booking_id)
    assert confirm_resp.status_code == 404


def test_update_booking_with_invalid_token(booking_api):
    # 1. Create a booking
    payload = sample_booking("Alice", "Smith")
    create_resp = booking_api.create(payload)
    assert create_resp.status_code == 200

    data = create_resp.json()
    booking_id = data["bookingid"]

    # 2. Try to update booking with invalid token
    token = "0"
    updated_payload = {**payload, "lastname": "Updated"}
    update_resp = booking_api.update(booking_id, updated_payload, token)
    assert update_resp.status_code == 403


def test_update_booking_with_invalid_id(booking_api, auth_api):
    # 1. Create a booking
    payload = sample_booking("Alice", "Smith")
    create_resp = booking_api.create(payload)
    assert create_resp.status_code == 200

    # 2. Try to update booking with invalid bookingId
    token = auth_api.create_token()
    updated_payload = {**payload, "lastname": "Updated"}
    update_resp = booking_api.update(99999, updated_payload, token)
    assert update_resp.status_code == 405


def test_delete_booking_with_invalid_token(booking_api):
    # 1. Create a booking
    payload = sample_booking("Alice", "Smith")
    create_resp = booking_api.create(payload)
    assert create_resp.status_code == 200

    data = create_resp.json()
    booking_id = data["bookingid"]

    # 2. Try to delete booking with invalid token
    token = "0"
    delete_resp = booking_api.delete(booking_id, token)
    assert delete_resp.status_code == 403


def test_delete_booking_with_invalid_id(booking_api, auth_api):
    token = auth_api.create_token()
    delete_resp = booking_api.delete(99999, token)
    assert delete_resp.status_code == 405
