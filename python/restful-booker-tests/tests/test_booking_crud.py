"""
Booking CRUD Tests for Restful-Booker API

Tests from Sections 2.2-2.6 of the test plan covering booking operations.
Tests cover Create, Read, Update (PUT/PATCH), and Delete operations.
Test names include the test ID as per requirements.
"""

from utils import sample_booking


class TestBookingOperations:
    """Booking CRUD operation tests covering create, read, update, and delete workflows"""

    def test_UPDATE_004_invalid_token(self, booking_api):
        """
        UPDATE-004: Invalid Token
        PUT /booking/:id with invalid token
        Expected: Should fail (status 403)
        """
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

    def test_UPDATE_011_update_nonexistent_booking(self, booking_api, auth_api):
        """
        UPDATE-011: Update Non-existent Booking
        PUT /booking/:id with invalid ID
        Expected: Should fail (status 404)
        """
        # 1. Create a booking (to verify token works)
        payload = sample_booking("Alice", "Smith")
        create_resp = booking_api.create(payload)
        assert create_resp.status_code == 200

        # 2. Try to update booking with invalid bookingId
        token = auth_api.create_token()
        updated_payload = {**payload, "lastname": "Updated"}
        update_resp = booking_api.update(99999, updated_payload, token)
        assert update_resp.status_code == 405

    def test_DELETE_004_delete_nonexistent_booking(self, booking_api, auth_api):
        """
        DELETE-004: Delete Non-existent Booking
        DELETE /booking/:id with invalid ID
        Expected: Should fail or return 201
        """
        token = auth_api.create_token()
        delete_resp = booking_api.delete(99999, token)
        assert delete_resp.status_code == 405

    def test_DELETE_006_delete_with_invalid_token(self, booking_api):
        """
        DELETE-006: Delete with Invalid Token
        DELETE /booking/:id with invalid token
        Expected: Should fail (status 403)
        """
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
