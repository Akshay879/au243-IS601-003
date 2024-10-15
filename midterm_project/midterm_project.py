import json
import os

def parse_orders(filename):
    assert os.path.exists(filename), f"File '{filename}' does not exist."
    with open(filename, 'r') as f:
        orders = json.load(f)
    
    customers = {order["phone"]: order["name"] for order in orders}
    with open('customers.json', 'w') as f:
        json.dump(customers, f, indent=4)