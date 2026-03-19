# users/api_documentation.py
"""
USERS APP API ENDPOINTS
=======================

BASE URL: http://localhost:8000/api/

1. GET ALL USERS
----------------
GET /users/
Query params: ?search=john&gender=male&page=1&page_size=10
Response: 200 OK

2. GET SINGLE USER
------------------
GET /users/{id}/
Example: GET /users/1/
Response: 200 OK

3. CREATE USER
--------------
POST /users/
Body: {
    "username": "john",
    "email": "john@email.com",
    "phone_number": "1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "age": 25,
    "gender": "male"
}
Response: 201 Created

4. UPDATE USER
--------------
PUT /users/{id}/
Body: (full user data)
Response: 200 OK

5. PARTIAL UPDATE
-----------------
PATCH /users/{id}/
Body: {"age": 26}
Response: 200 OK

6. DELETE USER
--------------
DELETE /users/{id}/
Response: 204 No Content

7. USER STATS
-------------
GET /users/stats/
Response: {
    "total_users": 10,
    "active_users": 8,
    "gender_stats": {...}
}
"""