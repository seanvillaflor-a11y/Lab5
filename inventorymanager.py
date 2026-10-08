#global constant
MAX_CAPACITY=500
TAX_RATE = 0.1
INVENTORY_FILE = "data/inventory.json"

import json

# ---------------------------------------------------------------
# Data persistence
# ---------------------------------------------------------------
def load_inventory():
    """Load inventory from INVENTORY_FILE if it exists, else return an empty list."""
    try:
        with open(INVENTORY_FILE, "r") as file:
            inventory = json.load(file)
        print(INVENTORY_FILE + " found.")
        print("Inventory loaded successfully.")
        return inventory
    except FileNotFoundError:
        print(INVENTORY_FILE + " not found. Starting with an empty inventory.")
        return []


def save_inventory(inventory):
    """Write the inventory list to INVENTORY_FILE as JSON."""
    print("Saving inventory...")
    try:
        with open(INVENTORY_FILE, "w") as file:
            json.dump(inventory, file, indent=4)
        print("Inventory saved successfully to " + INVENTORY_FILE + ".")
        return True
    except OSError as error:
        print("Error saving inventory: " + str(error))
        return False

# ==================
# data representation
# ==================

def load_starter_products(inventory):
    """Seed three starter products when there is no saved inventory."""
    starter = [
        ("P001", "Laptop", 1200.00, 15),
        ("P002", "Mouse", 25.50, 40),
        ("P003", "Keyboard", 45.00, 25),
    ]
    for product_id, name, price, stock in starter:
        inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})

#====================
# data manipulation
#====================
def find_product(inventory, product_id):
    """Return the product dictionary matching product_id, or None."""
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            return product
    return None


def add_product(inventory, product_id, name, price, stock):
    """Add a new product dictionary to the inventory list."""
    if find_product(inventory, product_id) is not None:
        print("Product ID already exists.")
        return False
    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
    })
    print("Product added successfully!")
    return True


def update_stock(inventory, product_id, new_stock):
    """Update the stock of an existing product."""
    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return False
    product["stock"] = new_stock
    print("Stock updated successfully!")
    return True


def search_product(inventory, product_id):
    """Display one product's details, or a not-found message."""
    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return None
    print("Product Found")
    print("-" * 48)
    print("ID: " + product["id"])
    print("Name: " + product["name"])
    print("Price: $" + format(product["price"], ".2f"))
    print("Stock: " + str(product["stock"]))
    print("-" * 48)
    return product


def display_all(inventory):
    """Display every product in the inventory."""
    print("Current Inventory")
    print("-" * 48)
    if not inventory:
        print("Inventory is empty.")
    for product in inventory:
        print("ID: " + product["id"]
              + " | Name: " + product["name"]
              + " | Price: $" + format(product["price"], ".2f")
              + " | Stock: " + str(product["stock"]))
    print("-" * 48)

# ---------------------------------------------------------------
# Menu GUI
# ---------------------------------------------------------------
def handle_add(inventory):
    print("Add New Product")
    product_id = input("Product ID: ").strip()
    if product_id == "":
        print("Product ID cannot be empty.")
        return
    name = input("Product Name: ").strip()
    if name == "":
        print("Product name cannot be empty.")
        return
    price = get_float("Price: ")
    stock = get_int("Stock Quantity: ")
    add_product(inventory, product_id, name, price, stock)


def handle_update(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print("Name: " + product["name"])
    print("Current Stock: " + str(product["stock"]))
    new_stock = get_int("New Stock Quantity: ")
    update_stock(inventory, product_id, new_stock)


def handle_search(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    search_product(inventory, product_id)


def print_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")




def get_valid_input():
        user_input = input("Enter stock quantity or type quit to exit: ")

        if user_input == "quit":
            return "quit"
        try:
            quantity = int(float(user_input)) # will accept decimal inputs, only ignore decimal and takes integer value
        except ValueError:
            print("Invalid input. please enter a number or type quit.")
            return None # invalidate output to avoid any rejected input to be added in data

        if quantity < 0 :
            print("invalid input. please enter a non-negative stock quantity")
            return None

        return quantity

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * TAX_RATE

def generate_report(total_units,rejected_attempts):
    print("\n--- Final Report ---")
    print("Total Deliveries Processed: " + str(total_units))
    print("Number of Failed/Rejected Entries: " + str(rejected_attempts))

#defining math of main into callable functions
def check_capacity(inventory, quantity):
    """Returns True if adding quantity would exceed MAX_CAPACITY."""
    return inventory + quantity > MAX_CAPACITY


def print_overstock_alert():
    print("Over stock alert! Maximum capacity is " + str(MAX_CAPACITY))


def print_delivery_summary(quantity, inventory, tax):
    print("Added " + str(quantity) + " items to inventory. Total Inventory: " + str(inventory))
    print("Tax on this delivery: $" + str(round(tax, 2)))


def print_final_summary(deliveries_processed, rejected, total_tax_collected):
    generate_report(deliveries_processed, rejected)
    print("Total tax collected: $" + str(round(total_tax_collected, 2)))



def main():
    inventory, transaction_history = load_inventory()
    deliveries_processed = 0
    rejected = 0
    total_tax_collected = 0.0

    while True:
        result = get_valid_input()

        if result == "quit":
            save_inventory(inventory, transaction_history)
            break

        if result is None:
            rejected += 1
            continue

        quantity = result
        
        if check_capacity(inventory, quantity):
            print_overstock_alert()
            rejected += 1
            break

        inventory = process_delivery(inventory, quantity)
        tax = calculate_tax(quantity)
        total_tax_collected += tax
        deliveries_processed += 1

        print_delivery_summary(quantity, inventory, tax)

    print_final_summary(deliveries_processed, rejected, total_tax_collected)


if __name__ == "__main__":
    main()