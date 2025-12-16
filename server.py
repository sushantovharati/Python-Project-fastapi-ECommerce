from fastapi import FastAPI
import threading, os

app = FastAPI(title="E-commerce API", version="1.1")

PRODUCT_FILE = "products.txt"
CUSTOMER_FILE = "customers.txt"
ORDER_FILE = "orders.txt"
lock = threading.Lock() 

# ------------------- File Helpers -------------------
def ensure_files():
    for f in [PRODUCT_FILE, CUSTOMER_FILE, ORDER_FILE]:
        if not os.path.exists(f):
            open(f, "w").close()

def read_file(file):
    with lock:
        if not os.path.exists(file):
            open(file, "w").close()
        with open(file, "r") as f:
            return [line.strip().split(",") for line in f.readlines() if line.strip()]

def write_file(file, rows):
    with lock:
        with open(file, "w") as f:
            f.write("\n".join([",".join(r) for r in rows]) + ("\n" if rows else ""))

# ------------------- Product Endpoints -------------------
@app.get("/products")
def list_products():
    rows = read_file(PRODUCT_FILE)
    return [{"id": r[0], "name": r[1], "price": r[2], "qty": r[3]} for r in rows]

@app.post("/products/add")
def add_product(id: str, name: str, price: str, qty: str):
    try:
        price = float(price)
        qty = int(qty)
    except ValueError:
        return {"error": "Price must be a number and Quantity must be an integer"}

    rows = read_file(PRODUCT_FILE)
    if any(r[0] == id for r in rows):
        return {"error": "Product ID already exists"}
    rows.append([id, name, str(price), str(qty)])
    write_file(PRODUCT_FILE, rows)
    return {"message": "Product added successfully"}

@app.post("/products/update")
def update_product(id: str, name: str, price: str, qty: str):
    try:
        price = float(price)
        qty = int(qty)
    except ValueError:
        return {"error": "Price must be a number and Quantity must be an integer"}

    rows = read_file(PRODUCT_FILE)
    for r in rows:
        if r[0] == id:
            r[1], r[2], r[3] = name, str(price), str(qty)
            write_file(PRODUCT_FILE, rows)
            return {"message": "Product updated"}
    return {"error": "Product not found"}

@app.delete("/products/delete")
def delete_product(id: str):
    rows = read_file(PRODUCT_FILE)
    new_rows = [r for r in rows if r[0] != id]
    write_file(PRODUCT_FILE, new_rows)
    return {"message": "Product deleted"}

# ------------------- Customer Endpoints -------------------
@app.get("/customers")
def list_customers():
    rows = read_file(CUSTOMER_FILE)
    return [{"id": r[0], "name": r[1], "phone": r[2]} for r in rows]

@app.post("/customers/add")
def add_customer(id: str, name: str, phone: str):
    rows = read_file(CUSTOMER_FILE)
    if any(r[0] == id for r in rows):
        return {"error": "Customer ID already exists"}
    rows.append([id, name, phone])
    write_file(CUSTOMER_FILE, rows)
    return {"message": "Customer added"}

@app.post("/customers/update")
def update_customer(id: str, name: str, phone: str):
    rows = read_file(CUSTOMER_FILE)
    for r in rows:
        if r[0] == id:
            r[1], r[2] = name, phone
            write_file(CUSTOMER_FILE, rows)
            return {"message": "Customer updated"}
    return {"error": "Customer not found"}

@app.delete("/customers/delete")
def delete_customer(id: str):
    rows = read_file(CUSTOMER_FILE)
    new_rows = [r for r in rows if r[0] != id]
    write_file(CUSTOMER_FILE, new_rows)
    return {"message": "Customer deleted"}

# ------------------- Order Endpoints -------------------
@app.get("/orders")
def list_orders():
    rows = read_file(ORDER_FILE)
    return [{"order_id": r[0], "customer_id": r[1], "product_id": r[2], "qty": r[3], "total": r[4]} for r in rows]

@app.post("/orders/create")
def create_order(order_id: str, customer_id: str, product_name: str, quantity: str):
    try:
        quantity = int(quantity)
        if quantity <= 0:
            return {"error": "Quantity must be a positive integer"}
    except ValueError:
        return {"error": "Quantity must be an integer"}

    orders = read_file(ORDER_FILE)
    if any(o[0] == order_id for o in orders):
        return {"error": "Order ID already exists"}

    products = read_file(PRODUCT_FILE)
    customers = read_file(CUSTOMER_FILE)
    if not any(c[0] == customer_id for c in customers):
        return {"error": "Customer not found"}

    product = next((p for p in products if p[1].lower() == product_name.lower()), None)
    if not product:
        return {"error": "Product not found"}

    if int(product[3]) < quantity:
        return {"error": "Not enough stock"}

    total_price = quantity * float(product[2])
    product[3] = str(int(product[3]) - quantity)
    write_file(PRODUCT_FILE, products)

    orders.append([order_id, customer_id, product[0], str(quantity), str(total_price)])
    write_file(ORDER_FILE, orders)

    return {"message": "Order created", "total_price": total_price}

@app.post("/orders/update")
def update_order(order_id: str, quantity: str):
    try:
        quantity = int(quantity)
        if quantity <= 0:
            return {"error": "Quantity must be a positive integer"}
    except ValueError:
        return {"error": "Quantity must be an integer"}

    orders = read_file(ORDER_FILE)
    products = read_file(PRODUCT_FILE)

    for o in orders:
        if o[0] == order_id:
            product = next((p for p in products if p[0] == o[2]), None)
            if not product:
                return {"error": "Product not found"}
            diff = quantity - int(o[3])
            if int(product[3]) < diff:
                return {"error": "Not enough stock to update"}
            product[3] = str(int(product[3]) - diff)
            o[3] = str(quantity)
            o[4] = str(float(product[2]) * quantity)
            write_file(PRODUCT_FILE, products)
            write_file(ORDER_FILE, orders)
            return {"message": "Order updated"}
    return {"error": "Order not found"}

@app.delete("/orders/delete")
def delete_order(order_id: str):
    orders = read_file(ORDER_FILE)
    products = read_file(PRODUCT_FILE)
    new_orders = []
    found = False
    for o in orders:
        if o[0] == order_id:
            found = True
            product = next((p for p in products if p[0] == o[2]), None)
            if product:
                product[3] = str(int(product[3]) + int(o[3]))
        else:
            new_orders.append(o)
    if not found:
        return {"error": "Order not found"}
    write_file(PRODUCT_FILE, products)
    write_file(ORDER_FILE, new_orders)
    return {"message": "Order deleted"}

ensure_files()
