import json
import os

def parse_orders(filename):
    assert os.path.exists(filename), f"File '{filename}' does not exist."
    with open(filename, 'r') as f:
        orders = json.load(f)
    
    customers = {order["phone"]: order["name"] for order in orders}
    with open('customers.json', 'w') as f:
        json.dump(customers, f, indent=4)

    summary = {}
    for order in orders:
        for item in order['items']:
            item_name = item['name']
            item_price = item['price']

            if item_name in summary:
                summary[item_name]['orders'] += 1
            else:
                summary[item_name] = {'price': item_price, 'orders': 1}

    with open('items.json','w') as f:
        json.dump(summary,f,indent=4)

parse_orders('example_orders.json')