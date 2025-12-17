# API Documentation

Complete reference for all ERP API endpoints and authentication.

## Base Information

- **Base URL**: `http://app-server-ip:8000/api/`
- **API Version**: v1 (via Accept header)
- **Content-Type**: `application/json`
- **Authentication**: JWT Bearer Token

## Authentication

### Obtain Tokens

#### Request

```bash
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

#### Response

```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refresh Access Token

#### Request

```bash
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

#### Response

```json
{
    "access": "new_access_token..."
}
```

### Using Token

Include in Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://app-server-ip:8000/api/hr/employees/
```

---

## HR Module (`/api/hr/`)

### Employees

#### List Employees

```bash
GET /api/hr/employees/
Authorization: Bearer TOKEN
```

Query Parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `department`: Filter by department
- `is_active`: Filter by active status (true/false)
- `search`: Search in name, email, employee_id

#### Response

```json
{
    "count": 50,
    "next": "http://.../api/hr/employees/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "employee_id": "EMP001",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "555-1234",
            "gender": "M",
            "date_of_birth": "1990-01-15",
            "date_joined": "2023-01-01",
            "department": "HR",
            "position": "HR Manager",
            "salary": "50000.00",
            "is_active": true,
            "created_at": "2023-01-01T10:00:00Z",
            "updated_at": "2023-01-01T10:00:00Z"
        }
    ]
}
```

#### Create Employee

```bash
POST /api/hr/employees/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "employee_id": "EMP002",
    "user": 2,
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com",
    "phone": "555-5678",
    "gender": "F",
    "date_of_birth": "1992-05-20",
    "date_joined": "2024-01-01",
    "department": "SALES",
    "position": "Sales Executive",
    "salary": "40000.00",
    "is_active": true
}
```

#### Retrieve Employee

```bash
GET /api/hr/employees/{id}/
Authorization: Bearer TOKEN
```

#### Update Employee

```bash
PUT /api/hr/employees/{id}/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "position": "Senior Sales Executive",
    "salary": "45000.00"
}
```

#### Delete Employee

```bash
DELETE /api/hr/employees/{id}/
Authorization: Bearer TOKEN
```

### Attendance

#### List Attendance Records

```bash
GET /api/hr/attendance/
Authorization: Bearer TOKEN
```

Query Parameters:
- `employee`: Filter by employee ID
- `status`: Filter by status (P/A/L/H)
- `date`: Filter by specific date (YYYY-MM-DD)

#### Create Attendance Record

```bash
POST /api/hr/attendance/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "employee": 1,
    "date": "2024-01-15",
    "status": "P",
    "check_in_time": "09:00:00",
    "check_out_time": "17:00:00",
    "remarks": "Regular working hours"
}
```

### Leaves

#### List Leave Requests

```bash
GET /api/hr/leaves/
Authorization: Bearer TOKEN
```

Query Parameters:
- `employee`: Filter by employee
- `leave_type`: Filter by type (SL/PL/CL/ML/UL)
- `status`: Filter by status (P/A/R)

#### Create Leave Request

```bash
POST /api/hr/leaves/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "employee": 1,
    "leave_type": "SL",
    "start_date": "2024-02-01",
    "end_date": "2024-02-02",
    "reason": "Medical appointment",
    "status": "P"
}
```

#### Approve Leave

```bash
POST /api/hr/leaves/{id}/approve/
Authorization: Bearer TOKEN
```

#### Reject Leave

```bash
POST /api/hr/leaves/{id}/reject/
Authorization: Bearer TOKEN
```

---

## Inventory Module (`/api/inventory/`)

### Products

#### List Products

```bash
GET /api/inventory/products/
Authorization: Bearer TOKEN
```

Query Parameters:
- `category`: Filter by category ID
- `search`: Search by name or code
- `page`: Page number

#### Create Product

```bash
POST /api/inventory/products/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "product_code": "PROD001",
    "name": "Widget A",
    "description": "High quality widget",
    "category": 1,
    "unit_price": "29.99",
    "reorder_level": 10,
    "current_stock": 50
}
```

### Stock Movements

#### List Stock Movements

```bash
GET /api/inventory/stock-movements/
Authorization: Bearer TOKEN
```

Query Parameters:
- `product`: Filter by product
- `movement_type`: Filter by type (IN/OUT/ADJUST)

#### Record Stock Movement

```bash
POST /api/inventory/stock-movements/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "product": 1,
    "movement_type": "IN",
    "quantity": 100,
    "reference_id": "PO-2024-001",
    "remarks": "Stock received from vendor"
}
```

### Categories

#### List Categories

```bash
GET /api/inventory/categories/
Authorization: Bearer TOKEN
```

#### Create Category

```bash
POST /api/inventory/categories/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "name": "Electronics",
    "description": "Electronic items and components"
}
```

---

## Finance Module (`/api/finance/`)

### Chart of Accounts

#### List Chart

```bash
GET /api/finance/charts/
Authorization: Bearer TOKEN
```

Query Parameters:
- `account_type`: Filter by account type

#### Create Chart Entry

```bash
POST /api/finance/charts/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "code": "1000",
    "name": "Cash",
    "account_type": "Asset",
    "description": "Cash and cash equivalents"
}
```

---

## Sales Module (`/api/sales/`)

### Customers

#### List Customers

```bash
GET /api/sales/customers/
Authorization: Bearer TOKEN
```

Query Parameters:
- `search`: Search by name, email, or phone
- `page`: Page number

#### Create Customer

```bash
POST /api/sales/customers/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "name": "ACME Corporation",
    "email": "info@acme.com",
    "phone": "555-9999",
    "address": "123 Business St",
    "city": "New York",
    "country": "USA"
}
```

#### Retrieve Customer

```bash
GET /api/sales/customers/{id}/
Authorization: Bearer TOKEN
```

---

## Procurement Module (`/api/procurement/`)

### Vendors

#### List Vendors

```bash
GET /api/procurement/vendors/
Authorization: Bearer TOKEN
```

Query Parameters:
- `search`: Search by name, email, or phone

#### Create Vendor

```bash
POST /api/procurement/vendors/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "name": "Reliable Suppliers Inc",
    "email": "contact@reliable.com",
    "phone": "555-8888",
    "address": "456 Supplier Ave",
    "rating": "4.50"
}
```

---

## Production Module (`/api/production/`)

### Work Orders

#### List Work Orders

```bash
GET /api/production/work-orders/
Authorization: Bearer TOKEN
```

Query Parameters:
- `status`: Filter by status (DRAFT/PLANNED/IN_PROGRESS/COMPLETED/CANCELLED)

#### Create Work Order

```bash
POST /api/production/work-orders/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "work_order_no": "WO-2024-001",
    "status": "DRAFT",
    "start_date": "2024-02-01",
    "end_date": "2024-02-15"
}
```

---

## Quality Module (`/api/quality/`)

### Quality Checks

#### List Quality Checks

```bash
GET /api/quality/checks/
Authorization: Bearer TOKEN
```

Query Parameters:
- `status`: Filter by status (PASSED/FAILED/PENDING)
- `check_date`: Filter by date

#### Create Quality Check

```bash
POST /api/quality/checks/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "check_date": "2024-01-20",
    "status": "PASSED",
    "remarks": "All quality parameters met"
}
```

---

## Maintenance Module (`/api/maintenance/`)

### Equipment

#### List Equipment

```bash
GET /api/maintenance/equipment/
Authorization: Bearer TOKEN
```

Query Parameters:
- `search`: Search by name or code

#### Create Equipment

```bash
POST /api/maintenance/equipment/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "code": "EQ-001",
    "name": "CNC Machine A",
    "description": "5-axis CNC machine",
    "location": "Building A - Floor 2"
}
```

### Maintenance Requests

#### List Maintenance Requests

```bash
GET /api/maintenance/requests/
Authorization: Bearer TOKEN
```

Query Parameters:
- `status`: Filter by status (OPEN/IN_PROGRESS/CLOSED)
- `priority`: Filter by priority (LOW/MEDIUM/HIGH)
- `equipment`: Filter by equipment

#### Create Maintenance Request

```bash
POST /api/maintenance/requests/
Authorization: Bearer TOKEN
Content-Type: application/json

{
    "ticket_no": "MR-2024-001",
    "equipment": 1,
    "status": "OPEN",
    "description": "Machine making unusual noise",
    "priority": "MEDIUM"
}
```

---

## Pagination

Most list endpoints support pagination:

```bash
GET /api/hr/employees/?page=2&page_size=50
```

Response includes:

```json
{
    "count": 150,
    "next": "http://.../api/hr/employees/?page=3",
    "previous": "http://.../api/hr/employees/?page=1",
    "results": [...]
}
```

---

## Filtering and Searching

### Filter Example

```bash
GET /api/hr/employees/?department=HR&is_active=true
```

### Search Example

```bash
GET /api/hr/employees/?search=john
```

### Combine Filters and Search

```bash
GET /api/hr/employees/?department=SALES&search=smith&page=2
```

---

## Error Responses

### 400 Bad Request

```json
{
    "email": [
        "This field may not be blank."
    ]
}
```

### 401 Unauthorized

```json
{
    "detail": "Invalid authentication credentials."
}
```

### 403 Forbidden

```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found

```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error

```json
{
    "detail": "Internal server error."
}
```

---

## Rate Limiting

API rate limits:
- **Anonymous users**: 100 requests/hour
- **Authenticated users**: 1000 requests/hour

Response headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1234567890
```

---

## Examples Using Different Clients

### cURL

```bash
TOKEN="your_access_token"

# Get employees
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/hr/employees/

# Create employee
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"employee_id":"EMP003","first_name":"Bob"}' \
  http://localhost:8000/api/hr/employees/
```

### Python Requests

```python
import requests

TOKEN = "your_access_token"
headers = {"Authorization": f"Bearer {TOKEN}"}

# Get employees
response = requests.get(
    "http://localhost:8000/api/hr/employees/",
    headers=headers
)
print(response.json())

# Create employee
data = {
    "employee_id": "EMP003",
    "first_name": "Bob",
    "last_name": "Johnson"
}
response = requests.post(
    "http://localhost:8000/api/hr/employees/",
    headers=headers,
    json=data
)
print(response.json())
```

### JavaScript/Fetch

```javascript
const TOKEN = "your_access_token";

// Get employees
fetch("http://localhost:8000/api/hr/employees/", {
    headers: {
        "Authorization": `Bearer ${TOKEN}`
    }
})
.then(r => r.json())
.then(data => console.log(data));

// Create employee
fetch("http://localhost:8000/api/hr/employees/", {
    method: "POST",
    headers: {
        "Authorization": `Bearer ${TOKEN}`,
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        employee_id: "EMP003",
        first_name: "Bob"
    })
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## API Versioning

Future versions will be accessed via:

```bash
GET /api/v2/hr/employees/
Accept: application/json; version=2
```

Current version (v1) is default.

---

## Additional Resources

- [Swagger/OpenAPI Documentation](http://localhost:8000/api/schema/swagger/)
- [ReDoc Documentation](http://localhost:8000/api/schema/redoc/)
- [Django REST Framework Guide](https://www.django-rest-framework.org/api-guide/)

---

**Note**: All timestamps are in UTC. Local timezone can be configured in settings.
