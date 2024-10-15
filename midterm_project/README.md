# Midterm Project: Order Processor

This Python script processes a JSON file containing customer orders and generates two output files:
1. `customers.json` - A JSON file with phone numbers as keys and customer names as values.
2. `items.json` - A JSON file summarizing the ordered items, including their prices and the number of times they were ordered.

## Script Overview

### What the Script Does
The script reads a JSON file containing a list of orders, where each order consists of a customer name, phone number, and a list of items purchased. It performs the following tasks:
- Extracts customer names and phone numbers, saving them to `customers.json`.
- Summarizes each item ordered, including the price and number of times it was ordered, and saves this summary to `items.json`.

### How the Script is Designed
The script is implemented with the following main steps:
1. **File Reading and Validation**:
   - Uses the `os` module to verify if the input file exists.
   - Reads the JSON file content using the `json` module.

2. **Creating the `customers.json` File**:
   - Extracts the `phone` and `name` fields from each order.
   - Creates a dictionary where the keys are phone numbers and the values are customer names.
   - Writes this dictionary to a file named `customers.json`.

3. **Creating the `items.json` File**:
   - Iterates through each order and counts how many times each item was ordered.
   - Uses a dictionary to keep track of the `price` and number of `orders` for each item.
   - Writes this summary to a file named `items.json`.

### How to Use the Script
1. **Prerequisites**:
   - Make sure you have Python installed (version 3.6 or above is recommended).

2. **Prepare the Input File**:
   - Create a JSON file (e.g., `example_orders.json`) that contains a list of orders. Each order should be a JSON object with the following structure:
     ```json
     [
        {
            "timestamp": 1702219784,
            "name": "Damodhar",
            "phone": "732-555-5509",
            "items": [
                {
                    "name": "Cheese Madurai Masala Dosa",
                    "price": 13.95
                },
                {
                    "name": "Onion Chilli Masala Dosa",
                    "price": 11.95
                }
            ],
            "notes": "extra spicy"
        },
        {
        "timestamp": 1684443264,
        "name": "Tom",
        "phone": "609-555-2301",
        "items": [
            {
                "name": "Cheese & Onion Chilli Masala Dosa",
                "price": 12.95
            },
            {
                "name": "Onion Rava Mysore Masala Dosa",
                "price": 14.95
            }
        ],
        "notes": ""
        }
    ]
     ```

3. **Run the Script**:
   - Execute the script from the command line or a Python environment:
     ```bash
     python midterm_project.py
     ```
   - Make sure to replace `example_orders.json` with the actual name of your file during function call

4. **Check the Output Files**:
   - After running the script, two new files, `customers.json` and `items.json`, will be created in the current directory.

## Example Output

### `customers.json`
```json
{
    "732-555-5509": "Damodhar",
    "609-555-2301": "Tom"
}

