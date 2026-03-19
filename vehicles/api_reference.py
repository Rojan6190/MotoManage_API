"""
VEHICLE APP API REFERENCE
=========================
Base URL: http://localhost:8000/api/

=================================
VEHICLE ENDPOINTS
=================================

1. GET ALL VEHICLES
-------------------
GET /vehicles/

Response 200 OK:
[
  {
    "id": 1,
    "owner": 1,
    "owner_username": "john_doe",
    "make": "Honda",
    "model": "Civic",
    "year": 2023,
    "vehicle_type": "four_wheeler",
    "fuel_type": "petrol"
  }
]

2. GET SINGLE VEHICLE
---------------------
GET /vehicles/{id}/
Example: GET /vehicles/1/

Response 200 OK:
{
  "id": 1,
  "owner": 1,
  "owner_username": "john_doe",
  "make": "Honda",
  "model": "Civic",
  "year": 2023,
  "vehicle_type": "four_wheeler",
  "fuel_type": "petrol"
}

3. CREATE VEHICLE
-----------------
POST /vehicles/
Content-Type: application/json

Request Body:
{
  "owner": 1,
  "make": "Toyota",
  "model": "Camry",
  "year": 2024,
  "vehicle_type": "four_wheeler",
  "fuel_type": "hybrid"
}

Vehicle Types:
- two_wheeler  -> "Two Wheeler"
- four_wheeler -> "Four Wheeler"
- heavy        -> "Heavy Vehicle"

Fuel Types:
- petrol  -> "Petrol"
- diesel  -> "Diesel"
- electric -> "Electric"

Response 201 Created:
{
  "id": 3,
  "owner": 1,
  "owner_username": "john_doe",
  "make": "Toyota",
  "model": "Camry",
  "year": 2024,
  "vehicle_type": "four_wheeler",
  "fuel_type": "hybrid"
}

4. UPDATE VEHICLE (FULL)
------------------------
PUT /vehicles/{id}/
Example: PUT /vehicles/1/

Request Body:
{
  "owner": 1,
  "make": "Honda",
  "model": "Accord",
  "year": 2024,
  "vehicle_type": "four_wheeler",
  "fuel_type": "hybrid"
}

Response 200 OK

5. PARTIAL UPDATE VEHICLE
-------------------------
PATCH /vehicles/{id}/
Example: PATCH /vehicles/1/

Request Body:
{
  "year": 2024,
  "fuel_type": "electric"
}

Response 200 OK

6. DELETE VEHICLE
-----------------
DELETE /vehicles/{id}/
Example: DELETE /vehicles/1/

Response 204 No Content

=================================
INSURANCE ENDPOINTS
=================================

7. GET ALL INSURANCE
--------------------
GET /insurances/

Response 200 OK:
[
  {
    "id": 1,
    "vehicle": 1,
    "policy_number": "INS-2024-001",
    "start_date": "2024-01-01",
    "expiry_date": "2025-01-01",
    "status": "active"
  }
]

8. GET SINGLE INSURANCE
-----------------------
GET /insurances/{id}/
Example: GET /insurances/1/

Response 200 OK:
{
  "id": 1,
  "vehicle": 1,
  "policy_number": "INS-2024-001",
  "start_date": "2024-01-01",
  "expiry_date": "2025-01-01",
  "status": "active"
}

9. GET INSURANCE BY VEHICLE
---------------------------
GET /vehicles/{vehicle_id}/insurance/
Example: GET /vehicles/1/insurance/

Response 200 OK:
{
  "id": 1,
  "vehicle": 1,
  "policy_number": "INS-2024-001",
  "start_date": "2024-01-01",
  "expiry_date": "2025-01-01",
  "status": "active"
}

Error 404:
{
  "detail": "No insurance found for this vehicle"
}

10. CREATE INSURANCE
--------------------
POST /insurances/
Content-Type: application/json

Request Body:
{
  "vehicle": 1,
  "policy_number": "INS-2024-002",
  "start_date": "2024-06-01",
  "expiry_date": "2025-06-01",
  "status": "active"
}

Status Options:
- active   -> "Active"
- expired  -> "Expired"
- pending  -> "Pending"

Response 201 Created:
{
  "id": 2,
  "vehicle": 1,
  "policy_number": "INS-2024-002",
  "start_date": "2024-06-01",
  "expiry_date": "2025-06-01",
  "status": "active"
}

11. UPDATE INSURANCE
--------------------
PUT /insurances/{id}/
Example: PUT /insurances/1/

Request Body:
{
  "vehicle": 1,
  "policy_number": "INS-2024-001-UPDATED",
  "start_date": "2024-01-01",
  "expiry_date": "2025-06-01",
  "status": "active"
}

Response 200 OK

12. PARTIAL UPDATE INSURANCE
----------------------------
PATCH /insurances/{id}/
Example: PATCH /insurances/1/

Request Body:
{
  "status": "expired"
}

Response 200 OK

13. DELETE INSURANCE
--------------------
DELETE /insurances/{id}/
Example: DELETE /insurances/1/

Response 204 No Content

=================================
FILTERING OPTIONS
=================================

Vehicle Filters:
----------------
GET /vehicles/?vehicle_type=four_wheeler
GET /vehicles/?fuel_type=electric
GET /vehicles/?owner=1
GET /vehicles/?search=Toyota

Insurance Filters:
------------------
GET /insurances/?status=active
GET /insurances/?vehicle=1
GET /insurances/?expiry_date__gte=2024-12-31
GET /insurances/?start_date__lte=2024-01-01

=================================
QUICK CURL COMMANDS
=================================

# Get all vehicles
curl http://localhost:8000/api/vehicles/

# Create vehicle
curl -X POST http://localhost:8000/api/vehicles/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "owner": 1,
    "make": "Honda",
    "model": "Civic",
    "year": 2023,
    "vehicle_type": "four_wheeler",
    "fuel_type": "petrol"
  }'

# Get vehicle insurance
curl http://localhost:8000/api/vehicles/1/insurance/

# Create insurance
curl -X POST http://localhost:8000/api/insurances/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "vehicle": 1,
    "policy_number": "TEST-001",
    "start_date": "2024-01-01",
    "expiry_date": "2025-01-01",
    "status": "active"
  }'

# Delete vehicle
curl -X DELETE http://localhost:8000/api/vehicles/1/

=================================
ERROR RESPONSES
=================================

400 Bad Request:
{
  "owner": ["Invalid pk \"99\" - object does not exist."],
  "year": ["Ensure this value is less than or equal to 2100."]
}

404 Not Found:
{
  "detail": "Not found."
}

=================================
"""