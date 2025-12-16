import requests

API = "http://127.0.0.1:8000"

# ------------------- HELPERS -------------------
def input_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer value.")

# ------------------- PRODUCT -------------------
def add_product():
    id = input("Product ID: ")
    name = input("Product Name: ")
    price = input_float("Price: ")
    qty = input_int("Quantity: ")
    res = requests.post(f"{API}/products/add", params={"id": id, "name": name, "price": price, "qty": qty})
    print(res.json())

def update_product():
    id = input("Enter Product ID to update: ")
    
    # Fetch current product info
    res = requests.get(f"{API}/products")
    products = res.json()
    product = next((p for p in products if p['id'] == id), None)
    if not product:
        print("Product not found.")
        return

    # Ask for new values, allow skipping
    name = input(f"New Name (current: {product['name']}): ") or product['name']

    # Updated numeric input with validation
    price_input = input(f"New Price (current: {product['price']}): ")
    try:
        price = float(price_input) if price_input else float(product['price'])
    except ValueError:
        print("Invalid price. Update cancelled.")
        return

    qty_input = input(f"New Quantity (current: {product['qty']}): ")
    try:
        qty = int(qty_input) if qty_input else int(product['qty'])
    except ValueError:
        print("Invalid quantity. Update cancelled.")
        return

    res = requests.post(f"{API}/products/update", params={"id": id, "name": name, "price": price, "qty": qty})
    print(res.json())


def delete_product():
    id = input("Product ID to delete: ")
    res = requests.delete(f"{API}/products/delete", params={"id": id})
    print(res.json())

def show_products():
    res = requests.get(f"{API}/products")
    data = res.json()
    if data:
        print("\n--- PRODUCT LIST ---")
        for r in data:
            print(f"ID: {r['id']}, Name: {r['name']}, Price: {r['price']}, Qty: {r['qty']}")
    else:
        print("No products found.")

# ------------------- CUSTOMER -------------------
def add_customer():
    id = input("Customer ID: ")
    name = input("Customer Name: ")
    phone = input("Phone Number: ")
    res = requests.post(f"{API}/customers/add", params={"id": id, "name": name, "phone": phone})
    print(res.json())

def update_customer():
    id = input("Customer ID to update: ")

    # Fetch current customer info
    res = requests.get(f"{API}/customers")
    customers = res.json()
    customer = next((c for c in customers if c['id'] == id), None)
    if not customer:
        print("Customer not found.")
        return

    # Ask for new values, allow skipping
    name = input(f"New Name (current: {customer['name']}): ") or customer['name']
    phone = input(f"New Phone (current: {customer['phone']}): ") or customer['phone']

    res = requests.post(f"{API}/customers/update", params={"id": id, "name": name, "phone": phone})
    print(res.json())


def delete_customer():
    id = input("Customer ID to delete: ")
    res = requests.delete(f"{API}/customers/delete", params={"id": id})
    print(res.json())

def show_customers():
    res = requests.get(f"{API}/customers")
    data = res.json()
    if data:
        print("\n--- CUSTOMER LIST ---")
        for r in data:
            print(f"ID: {r['id']}, Name: {r['name']}, Phone: {r['phone']}")
    else:
        print("No customers found.")

# ------------------- ORDERS -------------------
def create_order():
    order_id = input("Order ID: ")
    customer_id = input("Customer ID: ")
    product_name = input("Product Name: ")
    quantity = input_int("Quantity: ")
    res = requests.post(f"{API}/orders/create", params={
        "order_id": order_id,
        "customer_id": customer_id,
        "product_name": product_name,
        "quantity": quantity
    })
    print(res.json())

def update_order():
    order_id = input("Order ID to update: ")

    # Fetch current order info
    res = requests.get(f"{API}/orders")
    orders = res.json()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        print("Order not found.")
        return

    # Ask for new quantity, allow skipping
    qty_input = input(f"New Quantity (current: {order['qty']}): ")
    try:
        quantity = int(qty_input) if qty_input else int(order['qty'])
        if quantity <= 0:
            print("Quantity must be positive. Update cancelled.")
            return
    except ValueError:
        print("Invalid quantity. Update cancelled.")
        return

    res = requests.post(f"{API}/orders/update", params={"order_id": order_id, "quantity": quantity})
    print(res.json())


def delete_order():
    order_id = input("Order ID to delete: ")
    res = requests.delete(f"{API}/orders/delete", params={"order_id": order_id})
    print(res.json())

def show_orders():
    res = requests.get(f"{API}/orders")
    data = res.json()
    if data:
        print("\n--- ORDER LIST ---")
        for r in data:
            print(f"Order ID: {r['order_id']}, Customer ID: {r['customer_id']}, Product ID: {r['product_id']}, Qty: {r['qty']}, Total: {r['total']}")
    else:
        print("No orders found.")

# ------------------- MENUS -------------------
def admin_menu():
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. Product Management")
        print("2. Customer Management")
        print("3. Back")
        choice = input("Choose: ")
        if choice == "1": product_submenu()
        elif choice == "2": customer_submenu()
        elif choice == "3": break
        else: print("Invalid option")

def product_submenu():
    while True:
        print("\nProduct Management:")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. Show Product List")
        print("5. Back")
        choice = input("Choose: ")
        if choice == "1": add_product()
        elif choice == "2": update_product()
        elif choice == "3": delete_product()
        elif choice == "4": show_products()
        elif choice == "5": break
        else: print("Invalid option")

def customer_submenu():
    while True:
        print("\nCustomer Management:")
        print("1. Add Customer")
        print("2. Update Customer")
        print("3. Delete Customer")
        print("4. Show Customer List")
        print("5. Back")
        choice = input("Choose: ")
        if choice == "1": add_customer()
        elif choice == "2": update_customer()
        elif choice == "3": delete_customer()
        elif choice == "4": show_customers()
        elif choice == "5": break
        else: print("Invalid option")

def customer_menu():
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. Create Order")
        print("2. Update Order")
        print("3. Delete Order")
        print("4. Show Order List")
        print("5. Back")
        choice = input("Choose: ")
        if choice == "1": create_order()
        elif choice == "2": update_order()
        elif choice == "3": delete_order()
        elif choice == "4": show_orders()
        elif choice == "5": break
        else: print("Invalid option")

def main_menu():
    while True:
        print("\n==============================")
        print("        MAIN MENU")
        print("==============================")
        print("1. Admin")
        print("2. Customer")
        print("3. Exit")
        choice = input("Choose: ")
        if choice == "1": admin_menu()
        elif choice == "2": customer_menu()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main_menu()
