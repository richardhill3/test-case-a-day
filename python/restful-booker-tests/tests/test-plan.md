# Restful-Booker API Test Plan

## Document Overview
This test plan outlines comprehensive testing strategy for the Restful-Booker API v1.0.0.
The API provides booking management functionality with authentication, CRUD operations, and health check capabilities.

---

## 1. API Endpoints Summary

### 1.1 Auth Endpoints
- **POST /auth** - CreateToken
  - Purpose: Generate authentication token for protected operations
  - Required Headers: Content-Type: application/json
  - Request Body: username, password
  - Response: token

### 1.2 Booking Endpoints
- **GET /booking** - GetBookingIds
  - Purpose: Retrieve all booking IDs with optional filtering
  - Optional Query Parameters: firstname, lastname, checkin (CCYY-MM-DD), checkout (CCYY-MM-DD)
  - Response: Array of booking IDs

- **GET /booking/:id** - GetBooking
  - Purpose: Retrieve specific booking details
  - Headers: Accept (application/json or application/xml)
  - URL Parameter: id (booking ID)
  - Response: Booking object with all details

- **POST /booking** - CreateBooking
  - Purpose: Create a new booking
  - Headers: Content-Type, Accept (supports application/json, text/xml, url-encoded)
  - Request Body: firstname, lastname, totalprice, depositpaid, checkin, checkout, additionalneeds
  - Response: bookingid and booking object

- **PUT /booking/:id** - UpdateBooking (Full Update)
  - Purpose: Update entire booking record
  - Requires Authentication: Cookie token or Authorization (Basic auth)
  - Headers: Content-Type, Accept, Cookie/Authorization
  - URL Parameter: id
  - Request Body: All booking fields
  - Response: Updated booking object

- **PATCH /booking/:id** - PartialUpdateBooking
  - Purpose: Update specific fields of a booking
  - Requires Authentication: Cookie token or Authorization (Basic auth)
  - Headers: Content-Type, Accept, Cookie/Authorization
  - URL Parameter: id
  - Request Body: Any subset of booking fields (all optional)
  - Response: Updated booking object

- **DELETE /booking/:id** - DeleteBooking
  - Purpose: Delete a booking
  - Requires Authentication: Cookie token or Authorization (Basic auth)
  - Headers: Cookie/Authorization
  - URL Parameter: id
  - Response: HTTP 201 Created (success)

### 1.3 Health Check Endpoints
- **GET /ping** - HealthCheck
  - Purpose: Verify API is running
  - Response: HTTP 201 Created

---

## 2. Test Categories

### 2.1 Authentication Tests
| Test ID  | Test Name         | Description                                                       | Expected Result                           |
| -------- | ----------------- | ----------------------------------------------------------------- | ----------------------------------------- |
| AUTH-001 | Valid Credentials | POST /auth with valid username (admin) and password (password123) | Returns token string                      |
| AUTH-002 | Invalid Username  | POST /auth with incorrect username                                | Returns HTTP 200 with "Bad credentials"   |
| AUTH-003 | Invalid Password  | POST /auth with incorrect password                                | Returns HTTP 200 with "Bad credentials"   |
| AUTH-004 | Missing Username  | POST /auth without username field                                 | Returns HTTP 200 with "Bad credentials"   |
| AUTH-005 | Missing Password  | POST /auth without password field                                 | Returns HTTP 200 with "Bad credentials"   |
| AUTH-006 | Empty Credentials | POST /auth with empty username and password                       | Returns HTTP 200 with "Bad credentials"   |
| AUTH-007 | Token Persistence | Verify token can be used in subsequent requests                   | Token should work for protected endpoints |

### 2.2 Booking Creation Tests
| Test ID    | Test Name                | Description                                                | Expected Result                                      |
| ---------- | ------------------------ | ---------------------------------------------------------- | ---------------------------------------------------- |
| CREATE-001 | Create Valid Booking     | POST /booking with all required fields                     | Returns bookingid and booking object with status 200 |
| CREATE-002 | Create with JSON         | Create booking with application/json Content-Type          | Success with JSON response                           |
| CREATE-003 | Create with XML          | Create booking with text/xml Content-Type                  | Success with XML response                            |
| CREATE-004 | Create with URL Encoding | Create booking with url-encoded Content-Type               | Success with url-encoded response                    |
| CREATE-005 | Missing Required Field   | Create booking without firstname                           | Should fail (status 400)                             |
| CREATE-006 | Invalid Date Format      | Create booking with incorrect checkin/checkout date format | Should fail or use default format                    |
| CREATE-007 | Zero Price               | Create booking with totalprice = 0                         | Should succeed                                       |
| CREATE-008 | Negative Price           | Create booking with negative totalprice                    | Should fail or accept                                |
| CREATE-009 | Deposit Not Paid         | Create booking with depositpaid = false                    | Should succeed                                       |
| CREATE-010 | Additional Needs         | Create booking with additionalneeds field                  | Should accept and return in response                 |
| CREATE-011 | Empty String Fields      | Create booking with empty firstname/lastname               | Should accept or fail                                |
| CREATE-012 | Special Characters       | Create booking with special characters in names            | Should handle correctly                              |
| CREATE-013 | Very Long Names          | Create booking with extremely long firstname/lastname      | Should handle length limits                          |
| CREATE-014 | Date in Past             | Create booking with checkin/checkout in the past           | Should succeed                                       |
| CREATE-015 | Checkout Before Checkin  | Create booking where checkout date < checkin date          | Should fail or accept                                |

### 2.3 Booking Retrieval Tests
| Test ID | Test Name                | Description                                         | Expected Result                          |
| ------- | ------------------------ | --------------------------------------------------- | ---------------------------------------- |
| GET-001 | Get All Booking IDs      | GET /booking without filters                        | Returns array of all booking IDs         |
| GET-002 | Get Specific Booking     | GET /booking/:id with valid ID                      | Returns complete booking object          |
| GET-003 | Get Non-existent Booking | GET /booking/:id with invalid ID                    | Should fail (status 404)                 |
| GET-004 | Get as JSON              | GET /booking/:id with Accept: application/json      | Returns JSON response                    |
| GET-005 | Get as XML               | GET /booking/:id with Accept: application/xml       | Returns XML response                     |
| GET-006 | Filter by Firstname      | GET /booking?firstname=Sally                        | Returns only bookings matching firstname |
| GET-007 | Filter by Lastname       | GET /booking?lastname=Brown                         | Returns only bookings matching lastname  |
| GET-008 | Filter by Checkin Date   | GET /booking?checkin=2018-01-01                     | Returns bookings with checkin >= date    |
| GET-009 | Filter by Checkout Date  | GET /booking?checkout=2019-01-01                    | Returns bookings with checkout >= date   |
| GET-010 | Multiple Filters         | GET /booking with firstname AND lastname            | Returns intersection of filters          |
| GET-011 | Date Range Filter        | GET /booking with both checkin and checkout filters | Returns bookings within date range       |
| GET-012 | Invalid Date Format      | GET /booking with checkin in wrong format           | Should fail or use default behavior      |
| GET-013 | Non-existent Name Filter | GET /booking?firstname=NonExistent                  | Returns empty array                      |

### 2.4 Booking Update Tests (Full Update - PUT)
| Test ID    | Test Name                   | Description                                    | Expected Result                        |
| ---------- | --------------------------- | ---------------------------------------------- | -------------------------------------- |
| UPDATE-001 | Update with Token Auth      | PUT /booking/:id with valid token              | Returns updated booking                |
| UPDATE-002 | Update with Basic Auth      | PUT /booking/:id with Authorization header     | Returns updated booking                |
| UPDATE-003 | Update without Auth         | PUT /booking/:id without authentication        | Should fail (status 403)               |
| UPDATE-004 | Invalid Token               | PUT /booking/:id with invalid token            | Should fail (status 403)               |
| UPDATE-005 | Update Firstname            | PUT /booking/:id changing firstname            | Returns booking with updated firstname |
| UPDATE-006 | Update Lastname             | PUT /booking/:id changing lastname             | Returns booking with updated lastname  |
| UPDATE-007 | Update Price                | PUT /booking/:id changing totalprice           | Returns booking with updated price     |
| UPDATE-008 | Update Deposit Status       | PUT /booking/:id changing depositpaid          | Returns booking with updated status    |
| UPDATE-009 | Update Dates                | PUT /booking/:id changing checkin/checkout     | Returns booking with updated dates     |
| UPDATE-010 | Update Additional Needs     | PUT /booking/:id changing additionalneeds      | Returns booking with updated needs     |
| UPDATE-011 | Update Non-existent Booking | PUT /booking/:id with invalid ID               | Should fail (status 404)               |
| UPDATE-012 | JSON Response Format        | PUT /booking/:id with Accept: application/json | Returns JSON response                  |
| UPDATE-013 | XML Response Format         | PUT /booking/:id with Accept: application/xml  | Returns XML response                   |

### 2.5 Booking Partial Update Tests (PATCH)
| Test ID   | Test Name                  | Description                                        | Expected Result                         |
| --------- | -------------------------- | -------------------------------------------------- | --------------------------------------- |
| PATCH-001 | Partial Update with Token  | PATCH /booking/:id with token, update single field | Returns updated booking                 |
| PATCH-002 | Update Only Firstname      | PATCH /booking/:id with only firstname             | Other fields unchanged                  |
| PATCH-003 | Update Only Lastname       | PATCH /booking/:id with only lastname              | Other fields unchanged                  |
| PATCH-004 | Update Only Price          | PATCH /booking/:id with only totalprice            | Other fields unchanged                  |
| PATCH-005 | Update Only Checkin        | PATCH /booking/:id with only checkin               | Other fields unchanged                  |
| PATCH-006 | Update Multiple Fields     | PATCH /booking/:id with multiple optional fields   | Only specified fields updated           |
| PATCH-007 | Empty Patch Body           | PATCH /booking/:id with no fields                  | Should fail or return unchanged booking |
| PATCH-008 | Without Auth               | PATCH /booking/:id without authentication          | Should fail (status 403)                |
| PATCH-009 | Non-existent Booking       | PATCH /booking/:id with invalid ID                 | Should fail (status 404)                |
| PATCH-010 | Partial Update Persistence | Create, PATCH, GET to verify changes               | Changes should persist                  |

### 2.6 Booking Deletion Tests
| Test ID    | Test Name                   | Description                                   | Expected Result           |
| ---------- | --------------------------- | --------------------------------------------- | ------------------------- |
| DELETE-001 | Delete with Token Auth      | DELETE /booking/:id with valid token          | Returns HTTP 201 Created  |
| DELETE-002 | Delete with Basic Auth      | DELETE /booking/:id with Authorization header | Returns HTTP 201 Created  |
| DELETE-003 | Delete without Auth         | DELETE /booking/:id without authentication    | Should fail (status 403)  |
| DELETE-004 | Delete Non-existent Booking | DELETE /booking/:id with invalid ID           | Should fail or return 201 |
| DELETE-005 | Verify Deleted              | Create, DELETE, then GET same ID              | GET should return 404     |
| DELETE-006 | Delete with Invalid Token   | DELETE /booking/:id with invalid token        | Should fail (status 403)  |
| DELETE-007 | Double Delete               | DELETE same ID twice                          | Second delete should fail |

### 2.7 Health Check Tests
| Test ID    | Test Name            | Description                                                                     | Expected Result            |
| ---------- | -------------------- | ------------------------------------------------------------------------------- | -------------------------- |
| HEALTH-001 | Ping Response Status | GET /ping and verify HTTP 201 status code is returned with ok response          | Returns HTTP 201 Created   |
| HEALTH-002 | Ping Response Body   | GET /ping and verify response body contains success message ("Created" or "OK") | HTTP 201 with message body |

### 2.8 Integration Tests
| Test ID | Test Name               | Description                                      | Expected Result                             |
| ------- | ----------------------- | ------------------------------------------------ | ------------------------------------------- |
| INT-001 | Complete CRUD Flow      | Create → Read → Update → Delete → Verify         | All operations succeed in sequence          |
| INT-002 | Concurrent Bookings     | Create multiple bookings                         | All created with unique IDs                 |
| INT-003 | Filter After Creation   | Create booking, then filter by details           | Created booking appears in filtered results |
| INT-004 | Update After Create     | Create booking, update it, verify                | Changes persisted correctly                 |
| INT-005 | Partial Update Sequence | Create, PATCH multiple times, verify final state | All changes applied correctly               |
| INT-006 | Auth Token Expiry       | Create token, wait, use in request               | Verify token validity time                  |
| INT-007 | Update Previous Deleted | Create, delete, create new with same data        | New booking has different ID                |

### 2.9 Error Handling & Edge Cases
| Test ID   | Test Name                 | Description                                     | Expected Result                        |
| --------- | ------------------------- | ----------------------------------------------- | -------------------------------------- |
| ERROR-001 | Malformed JSON            | POST /booking with invalid JSON                 | Returns 400/422 error                  |
| ERROR-002 | Missing Content-Type      | POST /booking without Content-Type header       | Should use default or fail             |
| ERROR-003 | Invalid Accept Header     | GET /booking with unsupported Accept type       | Should fail or default to JSON         |
| ERROR-004 | Very Large Payload        | Create booking with extremely large name fields | Should fail with size limit or succeed |
| ERROR-005 | SQL Injection Attempt     | Try SQL injection in firstname field            | Should be sanitized/fail               |
| ERROR-006 | XSS Attempt               | Try XSS payload in firstname field              | Should be sanitized                    |
| ERROR-007 | Invalid Booking ID Format | GET /booking/abc (non-numeric)                  | Should fail (status 400)               |
| ERROR-008 | Negative ID               | GET /booking/-1                                 | Should fail or return 404              |
| ERROR-009 | Float ID                  | GET /booking/1.5                                | Should fail or parse as integer        |
| ERROR-010 | Unicode Characters        | Create booking with unicode in names            | Should handle or reject                |

### 2.10 Data Validation Tests
| Test ID   | Test Name              | Description                            | Expected Result                      |
| --------- | ---------------------- | -------------------------------------- | ------------------------------------ |
| VALID-001 | Field Type: String     | firstname should be string type        | Accept string, reject numbers        |
| VALID-002 | Field Type: Number     | totalprice should be number            | Accept number, reject strings        |
| VALID-003 | Field Type: Boolean    | depositpaid should be boolean          | Accept true/false, reject strings    |
| VALID-004 | Field Type: Date       | Dates should be in CCYY-MM-DD format   | Accept valid dates, reject invalid   |
| VALID-005 | Date Format Validation | Verify checkin/checkout are CCYY-MM-DD | Reject other formats                 |
| VALID-006 | Price Precision        | totalprice with decimal values         | Should handle decimal precision      |
| VALID-007 | Maximum Values         | Test with maximum allowed values       | Should accept or reject consistently |
| VALID-008 | Minimum Values         | Test with minimum values (0, 1, etc.)  | Should accept or reject consistently |

---

## 3. Test Data Requirements

### 3.1 Sample Test Data
```json
{
  "validBooking": {
    "firstname": "Jim",
    "lastname": "Brown",
    "totalprice": 111,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2018-01-01",
      "checkout": "2019-01-01"
    },
    "additionalneeds": "Breakfast"
  },
  "credentials": {
    "username": "admin",
    "password": "password123"
  }
}
```

### 3.2 Authentication Credentials
- Default Username: `admin`
- Default Password: `password123`
- Alternative Auth Method: Basic Auth header with base64 encoded credentials

---

## 4. Testing Approach

### 4.1 Test Execution Order
1. **Health Check** - Verify API is available
2. **Authentication** - Obtain token for protected operations
3. **Create Operations** - Establish test data
4. **Read Operations** - Verify data retrieval
5. **Update Operations** - Test data modification
6. **Delete Operations** - Clean up test data
7. **Integration Tests** - End-to-end workflows
8. **Error Cases** - Verify error handling

### 4.2 Test Environment
- Base URL: `https://restful-booker.herokuapp.com`
- API Version: 1.0.0
- Content Types: application/json (primary), application/xml, url-encoded
- Authentication: Token-based (Cookie) or Basic Auth

### 4.3 Success Criteria
- All endpoints return expected HTTP status codes
- Response structures match documentation
- All data fields are properly validated
- Authentication is properly enforced on protected endpoints
- Filtering and search operations work as documented
- Error messages are meaningful and consistent

---

## 5. Risk Areas & Known Considerations

### 5.1 Potential Issues
1. **Date Format Handling** - Verify strict CCYY-MM-DD format enforcement
2. **Authentication Token Lifecycle** - Unclear if tokens expire
3. **Concurrent Updates** - No conflict resolution mentioned
4. **Data Persistence** - Unclear if data persists across API restarts
5. **Rate Limiting** - No mention of rate limits in documentation
6. **Field Length Limits** - Maximum string lengths not specified
7. **Price Precision** - Decimal handling not explicitly documented
8. **Delete Response Status** - Returns 201 instead of typical 204/200
9. **Auth Endpoint Response Behavior** - Returns HTTP 200 with "Bad credentials" message for all invalid auth attempts (missing, empty, incorrect fields) instead of HTTP 400/401/403

### 5.2 Assumptions
- Token from /auth endpoint is case-sensitive
- All dates follow CCYY-MM-DD format strictly
- Empty arrays in filter results indicate no matches
- Basic auth uses base64 encoding of username:password
- All fields in request body are optional except during full updates (PUT)

---

## 6. Test Execution Notes

### 6.1 Dependencies
- Valid authentication token required for PUT, PATCH, DELETE operations
- Test bookings should be created before testing retrieval
- Cleanup: Delete test bookings after execution

### 6.2 Reporting
- Document response times for performance baseline
- Track any deviations from documented behavior
- Log all 4xx and 5xx responses for analysis
- Verify consistency of response structure across all endpoints

---

## 7. Test Coverage Summary

| Category               | Test Count | Priority |
| ---------------------- | ---------- | -------- |
| Authentication         | 7          | High     |
| Create Operations      | 14         | High     |
| Read Operations        | 13         | High     |
| Update (PUT)           | 13         | High     |
| Partial Update (PATCH) | 10         | Medium   |
| Delete Operations      | 7          | High     |
| Health Check           | 2          | Low      |
| Integration            | 7          | High     |
| Error Handling         | 10         | High     |
| Data Validation        | 8          | Medium   |
| **Total**              | **91**     | -        |

---

**Document Version:** 1.0  
**Created:** November 15, 2025  
**API Version:** 1.0.0  
**API Documentation URL:** http://localhost:3001/apidoc/index.html
