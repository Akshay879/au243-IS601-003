from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

app = FastAPI()

DATABASE = "db.sqlite"

# Pydantic Models
class Customer(BaseModel):
    name: str
    phone: str

class Item(BaseModel):
    name: str
    price: float

class OrderItem(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    customer_id: int
    timestamp: int
    notes: str = None
    items: list[OrderItem]

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Customers Endpoints
@app.get("/customers")
def list_customers(
    skip: int = 0, 
    limit: int = 10, 
    name: Optional[str] = None, 
    phone: Optional[str] = None
):
    
    if skip < 0 or limit < 1:
        raise HTTPException(status_code=422, detail="Invalid pagination parameters.")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM customers WHERE 1=1"
    params = []
    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    
    if phone:
        query += " AND phone LIKE ?"
        params.append(f"%{phone}%")
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, skip])
    
    cursor.execute(query, tuple(params))
    customers = cursor.fetchall()
    conn.close()
    
    return {
        "customers": [{"id": customer[0], "name": customer[1], "phone": customer[2]} for customer in customers]
    }

@app.post("/customers")
def create_customer(customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Customer with this phone number already exists.")
    finally:
        conn.close()
    return {"message": "Customer created successfully."}

@app.get("/customers/{id}")
def get_customer(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (id,))
    customer = cursor.fetchone()
    conn.close()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return dict(customer)

@app.put("/customers/{id}")
def update_customer(id: int, customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (customer.name, customer.phone, id))
    conn.commit()
    conn.close()
    return {"message": "Customer updated successfully."}

@app.delete("/customers/{id}")
def delete_customer(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Customer deleted successfully."}

# Items Endpoints with Pagination and Filtering
@app.get("/items")
def list_items(skip: int = 0, limit: int = 10, name: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM items WHERE 1=1"
    
    params = []
    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if min_price:
        query += " AND price >= ?"
        params.append(min_price)
    if max_price:
        query += " AND price <= ?"
        params.append(max_price)
    
    query += " LIMIT ? OFFSET ?"
    params += [limit, skip]
    
    cursor.execute(query, params)
    items = cursor.fetchall()
    conn.close()
    
    return {"items": [dict(item) for item in items]}

@app.post("/items")
def create_item(item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
    conn.commit()
    conn.close()
    return {"message": "Item created successfully."}

@app.get("/items/{id}")
def get_item(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (id,))
    item = cursor.fetchone()
    conn.close()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    return dict(item)

@app.put("/items/{id}")
def update_item(id: int, item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (item.name, item.price, id))
    conn.commit()
    conn.close()
    return {"message": "Item updated successfully."}

@app.delete("/items/{id}")
def delete_item(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Item deleted successfully."}

# Orders Endpoints
# GET: List orders with pagination
@app.get("/orders")
def list_orders(skip: int = 0, limit: int = 10):
    if skip < 0 or limit < 1:
        raise HTTPException(status_code=422, detail="Invalid skip or limit value.")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders LIMIT ? OFFSET ?", (limit, skip))
    orders = cursor.fetchall()
    conn.close()
    
    return {"orders": [dict(order) for order in orders]}

@app.post("/orders")
def create_order(order: Order):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert order
    cursor.execute("INSERT INTO orders (customer_id, timestamp, notes) VALUES (?, ?, ?)",
                   (order.customer_id, order.timestamp, order.notes))
    order_id = cursor.lastrowid
    # Insert items
    for item in order.items:
        cursor.execute("INSERT OR IGNORE INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
        cursor.execute("SELECT id FROM items WHERE name = ?", (item.name,))
        item_id = cursor.fetchone()["id"]
        cursor.execute("INSERT INTO order_items (order_id, item_id) VALUES (?, ?)", (order_id, item_id))
    conn.commit()
    conn.close()
    return {"message": "Order created successfully."}

@app.get("/orders/{id}")
def get_order(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Fetch order details
    cursor.execute("SELECT * FROM orders WHERE id = ?", (id,))
    order = cursor.fetchone()
    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found.")
    # Fetch items in the order
    cursor.execute("""
        SELECT items.name, items.price
        FROM order_items
        JOIN items ON order_items.item_id = items.id
        WHERE order_items.order_id = ?
    """, (id,))
    items = cursor.fetchall()
    conn.close()
    return {"order": dict(order), "items": [dict(item) for item in items]}

@app.put("/orders/{id}")
def update_order(id: int, order: Order):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Update order
    cursor.execute("UPDATE orders SET customer_id = ?, timestamp = ?, notes = ? WHERE id = ?",
                   (order.customer_id, order.timestamp, order.notes, id))
    # Update items (simplified logic: delete and recreate links)
    cursor.execute("DELETE FROM order_items WHERE order_id = ?", (id,))
    for item in order.items:
        cursor.execute("INSERT OR IGNORE INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
        cursor.execute("SELECT id FROM items WHERE name = ?", (item.name,))
        item_id = cursor.fetchone()["id"]
        cursor.execute("INSERT INTO order_items (order_id, item_id) VALUES (?, ?)", (id, item_id))
    conn.commit()
    conn.close()
    return {"message": "Order updated successfully."}

@app.delete("/orders/{id}")
def delete_order(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Order deleted successfully."}

