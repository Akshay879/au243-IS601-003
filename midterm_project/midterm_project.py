import json
import os

def parse_orders(filename):
    assert os.path.exists(filename), f"File '{filename}' does not exist."
    with open(filename, 'r') as f:
        orders = json.load(f)
    print(orders)

parse_orders("example_orders.json")