def sample_booking(first="John", last="Doe"):
    return {
        "firstname": first,
        "lastname": last,
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {"checkin": "2025-12-01", "checkout": "2025-12-05"},
        "additionalneeds": "Breakfast",
    }
