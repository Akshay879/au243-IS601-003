from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

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

# Items Endpoints
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

