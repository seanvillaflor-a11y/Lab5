import json

# Global constant
INVENTORY_FILE = "inventory.json"


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
    except (json.JSONDecodeError, OSError):
        print("Could not read " + INVENTORY_FILE + ". Starting with an empty inventory.")
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


# ---------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------
def get_float(prompt):
    """Keep asking until the user enters a non-negative number."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Invalid input. Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_int(prompt):
    """Keep asking until the user enters a non-negative whole number."""
    while True:
        try:
            value = int(float(input(prompt)))  # decimals are truncated
            if value < 0:
                print("Invalid input. Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


# ---------------------------------------------------------------
# Data manipulation (CRUD)
# ---------------------------------------------------------------
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
# Menu handlers
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


def load_starter_products(inventory):
    """Seed three starter products when there is no saved inventory."""
    starter = [
        ("P001", "Laptop", 1200.00, 15),
        ("P002", "Mouse", 25.50, 40),
        ("P003", "Keyboard", 45.00, 25),
    ]
    for product_id, name, price, stock in starter:
        inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()
    if not inventory:
        load_starter_products(inventory)
        print("Loaded 3 starter products.")

    print_menu()

    while True:
        try:
            option = input("Enter option: ").strip()
        except EOFError:
            option = "6"

        if option == "1":
            display_all(inventory)
        elif option == "2":
            handle_add(inventory)
        elif option == "3":
            handle_update(inventory)
        elif option == "4":
            handle_search(inventory)
        elif option == "5":
            save_inventory(inventory)
        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()