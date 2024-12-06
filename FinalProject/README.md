# Dosa Restaurant

This project provides a RESTful API built with **FastAPI** and **SQLite** for managing customers, items, and orders. It demonstrates a clean and modular design for building and interacting with a relational database using FastAPI's capabilities. 

## Features
The API supports the following operations:
- **Customers**:
  - List customers with optional filters (name, phone) and pagination.
  - Create, retrieve, update, and delete customer records.
- **Items**:
  - List items with filters (name, price range) and pagination.
  - Create, retrieve, update, and delete item records.
- **Orders**:
  - List orders with pagination.
  - Create, retrieve, update, and delete orders.
  - Manage order-item relationships.
  
---

## Project Structure

### Database
The database consists of four tables:
1. **Customers**: Stores customer details like name and phone number.
2. **Items**: Stores information about items like name and price.
3. **Orders**: Tracks orders with references to customers, timestamps, and optional notes.
4. **Order Items**: Represents a many-to-many relationship between orders and items.

### API Design
The API is structured into three major sections:
1. **Customer Endpoints**:
   - `/customers`: CRUD operations with optional filtering and pagination.
2. **Item Endpoints**:
   - `/items`: CRUD operations with optional filtering (name, price range) and pagination.
3. **Order Endpoints**:
   - `/orders`: CRUD operations for managing orders, including order-item relationships.

---

## Setup

### Prerequisites
- Python 3.9+
- Pip (Python package manager)

### Setup
1. Initalize the database.
    ```bash
    python init_db.py
    python main.py
    ```
2. Start the FastAPI application.
    ```bash
    uvicorn main:app --reload
    ```

### API Endpoints
1. Customers
| Method |	Endpoint |	Description
| GET    | /customers|	List customers with optional filters.
| POST   | /customers|	Create a new customer.
| GET    | /customers/{id}|	Retrieve a customer by ID.
| PUT	 | /customers/{id}|	Update a customer's details by ID.
| DELETE | /customers/{id}|	Delete a customer by ID.
Example: Create a New Customer
Request:
    ```json
    POST /customers
    {
    "name": "John Doe",
    "phone": "1234567890"
    }
    ```
Response:
    ```json
    {
    "message": "Customer created successfully."
    }
    ```

2. Items
|Method	 | Endpoint | Description
|GET	 | /items	| List items with filters and pagination.
|POST	 | /items	| Create a new item.
|GET	 | /items/{id}|	Retrieve an item by ID.
|PUT	 | /items/{id}|	Update an item by ID.
|DELETE	 | /items/{id}|	Delete an item by ID.
Example: List Items with Filters
Request:
    ```json
    GET /items?name=phone&min_price=100
    ```
Response:
    ```json
    {
  "items": [
    {"id": 1, "name": "Smartphone", "price": 299.99},
    {"id": 2, "name": "Phone Cover", "price": 19.99}
        ]
    }
    ```

3. Orders
|Method | Endpoint|	Description
|GET	| /orders |	List orders with pagination.
|POST	| /orders |	Create a new order with items.
|GET	|/orders/{id}|	Retrieve an order and its items by ID.
|PUT	|/orders/{id}|	Update an order and its items by ID.
|DELETE	|/orders/{id}|	Delete an order by ID.
Example: Create a New Order
Request:
    ```json
    POST /orders
    {
    "customer_id": 1,
    "timestamp": 1700000000,
    "notes": "Please deliver quickly.",
    "items": [
        {"name": "Laptop", "price": 899.99},
        {"name": "Mouse", "price": 29.99}
        ]
    }
    ```
Response:
    ```json
    {
    "message": "Order created successfully."
    }
    ```

### Usage Notes

## Pagination
Endpoints that support pagination (skip and limit) allow you to fetch records in chunks. For example:
    ```bash
    GET /customers?skip=0&limit=5
    ```

## Filtering
Filters (like name, phone, min_price, max_price) allow narrowing down search results. For example:
    ```bash
    GET /items?name=phone&min_price=50&max_price=300
    ```

## Testing the API
After running the server, visit the interactive API documentation at:

Swagger UI: http://127.0.0.1:8000/docs