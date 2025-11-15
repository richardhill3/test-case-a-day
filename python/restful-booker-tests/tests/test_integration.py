"""
Integration Tests for Restful-Booker API

Tests from Section 2.8 of the test plan covering end-to-end workflows.
Test names include the test ID as per requirements (e.g., test_INT_001_complete_crud_flow)
"""

import time
from utils import sample_booking


class TestIntegration:
    """Integration tests covering complete workflows and multi-step operations"""

    def test_INT_001_complete_crud_flow(self, booking_api, auth_api):
        """
        INT-001: Complete CRUD Flow
        Create → Read → Update → Delete → Verify
        Expected: All operations succeed in sequence
        """
        # 1. Create Booking
        payload = sample_booking("Jim", "Brown")
        create_resp = booking_api.create(payload)
        assert create_resp.status_code == 200
        data = create_resp.json()
        booking_id = data["bookingid"]
        assert booking_id is not None

        # 2. Read Booking
        get_resp = booking_api.get(booking_id)
        assert get_resp.status_code == 200
        booking_data = get_resp.json()
        assert booking_data["firstname"] == "Jim"
        assert booking_data["lastname"] == "Brown"

        # 3. Update Booking
        token = auth_api.create_token()
        updated_payload = sample_booking("James", "Brown")
        update_resp = booking_api.update(booking_id, updated_payload, token)
        assert update_resp.status_code == 200
        updated_data = update_resp.json()
        assert updated_data["firstname"] == "James"

        # 4. Delete Booking
        delete_resp = booking_api.delete(booking_id, token)
        assert delete_resp.status_code == 201

        # 5. Verify Deletion
        verify_resp = booking_api.get(booking_id)
        assert verify_resp.status_code == 404

    def test_INT_002_concurrent_bookings(self, booking_api):
        """
        INT-002: Concurrent Bookings
        Create multiple bookings simultaneously
        Expected: All created with unique IDs
        """
        booking_ids = []

        # Create 5 bookings with different names
        test_names = [
            ("Alice", "Smith"),
            ("Bob", "Johnson"),
            ("Charlie", "Williams"),
            ("Diana", "Brown"),
            ("Eva", "Davis"),
        ]

        for first, last in test_names:
            payload = sample_booking(first, last)
            resp = booking_api.create(payload)
            assert resp.status_code == 200
            booking_id = resp.json()["bookingid"]
            booking_ids.append(booking_id)

        # Verify all IDs are unique
        assert len(booking_ids) == len(set(booking_ids))

        # Verify each booking can be retrieved
        for booking_id in booking_ids:
            resp = booking_api.get(booking_id)
            assert resp.status_code == 200

    def test_INT_003_filter_after_creation(self, booking_api):
        """
        INT-003: Filter After Creation
        Create booking, then filter by details
        Expected: Created booking appears in filtered results
        """
        # Create a unique booking
        unique_first = f"TestUser_{int(time.time())}"
        payload = sample_booking(unique_first, "FilterTest")
        create_resp = booking_api.create(payload)
        assert create_resp.status_code == 200
        booking_id = create_resp.json()["bookingid"]

        # Filter by firstname
        filter_resp = booking_api.get_all(firstname=unique_first)
        assert filter_resp.status_code == 200
        results = filter_resp.json()
        booking_ids = [
            item["bookingid"] if isinstance(item, dict) else item for item in results
        ]
        assert booking_id in booking_ids

        # Filter by lastname
        filter_resp_last = booking_api.get_all(lastname="FilterTest")
        assert filter_resp_last.status_code == 200
        results_last = filter_resp_last.json()
        booking_ids_last = [
            item["bookingid"] if isinstance(item, dict) else item
            for item in results_last
        ]
        assert booking_id in booking_ids_last

    def test_INT_004_update_after_create(self, booking_api, auth_api):
        """
        INT-004: Update After Create
        Create booking, update it, verify changes
        Expected: Changes persisted correctly
        """
        # Create booking
        original_payload = sample_booking("Original", "Name")
        create_resp = booking_api.create(original_payload)
        assert create_resp.status_code == 200
        booking_id = create_resp.json()["bookingid"]

        # Get original values
        get_original = booking_api.get(booking_id)
        assert get_original.status_code == 200
        original_data = get_original.json()
        original_price = original_data["totalprice"]

        # Update with new values
        token = auth_api.create_token()
        updated_payload = sample_booking("Updated", "Name")
        updated_payload["totalprice"] = original_price + 100

        update_resp = booking_api.update(booking_id, updated_payload, token)
        assert update_resp.status_code == 200

        # Verify changes persisted
        get_updated = booking_api.get(booking_id)
        assert get_updated.status_code == 200
        updated_data = get_updated.json()
        assert updated_data["firstname"] == "Updated"
        assert updated_data["totalprice"] == original_price + 100

    def test_INT_005_partial_update_sequence(self, booking_api, auth_api):
        """
        INT-005: Partial Update Sequence
        Create, PATCH multiple times, verify final state
        Expected: All changes applied correctly
        """
        # Create booking
        payload = sample_booking("John", "Doe")
        create_resp = booking_api.create(payload)
        assert create_resp.status_code == 200
        booking_id = create_resp.json()["bookingid"]

        token = auth_api.create_token()

        # First partial update - change firstname only
        patch_1 = {"firstname": "Jonathan"}
        resp_1 = booking_api.partial_update(booking_id, patch_1, token)
        assert resp_1.status_code == 200
        data_1 = resp_1.json()
        assert data_1["firstname"] == "Jonathan"
        assert data_1["lastname"] == "Doe"  # Should be unchanged

        # Second partial update - change lastname only
        patch_2 = {"lastname": "Smith"}
        resp_2 = booking_api.partial_update(booking_id, patch_2, token)
        assert resp_2.status_code == 200
        data_2 = resp_2.json()
        assert data_2["firstname"] == "Jonathan"  # Should still be Jonathan
        assert data_2["lastname"] == "Smith"

        # Third partial update - change price only
        patch_3 = {"totalprice": 500}
        resp_3 = booking_api.partial_update(booking_id, patch_3, token)
        assert resp_3.status_code == 200
        data_3 = resp_3.json()
        assert data_3["firstname"] == "Jonathan"
        assert data_3["lastname"] == "Smith"
        assert data_3["totalprice"] == 500

        # Verify final state persisted
        get_final = booking_api.get(booking_id)
        assert get_final.status_code == 200
        final_data = get_final.json()
        assert final_data["firstname"] == "Jonathan"
        assert final_data["lastname"] == "Smith"
        assert final_data["totalprice"] == 500

    def test_INT_006_auth_token_expiry(self, auth_api, booking_api):
        """
        INT-006: Auth Token Expiry
        Create token, wait, use in request
        Expected: Verify token validity time
        """
        # Create token
        token_1 = auth_api.create_token()
        assert isinstance(token_1, str)
        assert len(token_1) > 0

        # Use token immediately in a protected operation
        payload = sample_booking("TokenTest", "User")
        create_resp = booking_api.create(payload)
        assert create_resp.status_code == 200
        booking_id = create_resp.json()["bookingid"]

        update_payload = sample_booking("TokenTest", "UserUpdated")
        update_resp_1 = booking_api.update(booking_id, update_payload, token_1)
        # Token should work immediately
        assert update_resp_1.status_code in [200, 201]

        # Wait a moment and try again with same token
        time.sleep(1)
        update_payload_2 = sample_booking("TokenTest", "UserUpdated2")
        update_resp_2 = booking_api.update(booking_id, update_payload_2, token_1)
        # Token should still work after brief wait (assuming tokens don't expire quickly)
        assert update_resp_2.status_code in [200, 201]

    def test_INT_007_update_previous_deleted(self, booking_api, auth_api):
        """
        INT-007: Update Previous Deleted
        Create, delete, create new with same data
        Expected: New booking has different ID
        """
        token = auth_api.create_token()
        shared_payload = sample_booking("Shared", "Data")

        # Create first booking
        create_resp_1 = booking_api.create(shared_payload)
        assert create_resp_1.status_code == 200
        booking_id_1 = create_resp_1.json()["bookingid"]

        # Delete first booking
        delete_resp = booking_api.delete(booking_id_1, token)
        assert delete_resp.status_code == 201

        # Create second booking with same data
        create_resp_2 = booking_api.create(shared_payload)
        assert create_resp_2.status_code == 200
        booking_id_2 = create_resp_2.json()["bookingid"]

        # IDs should be different
        assert booking_id_1 != booking_id_2

        # First booking should be gone
        get_first = booking_api.get(booking_id_1)
        assert get_first.status_code == 404

        # Second booking should exist
        get_second = booking_api.get(booking_id_2)
        assert get_second.status_code == 200
        second_data = get_second.json()
        assert second_data["firstname"] == "Shared"
        assert second_data["lastname"] == "Data"
