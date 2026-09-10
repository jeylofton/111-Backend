from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__) # Instance of Flask


DB_NAME = "online-store.db"


def init_db():
    connection = sqlite3.connect(DB_NAME) # Opens the connection to the D.B. files named 'online-store.db'
    cursor = connection.cursor() # Creates a cursor/tool that lets us send commands (Select/Insert,...) to the D.B.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        discount INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL,
        category TEXT NOT NULL,
        image TEXT NOT NULL
    )
    """)


    connection.commit() # Save changes to the D.B.
    connection.close() # Close the connection to the D.B.


@app.get("/api/health")
def health_check():
    return jsonify({"status": "Ok"}), 200

# ----- PRODUCTS -----
# POST /api/products -> creation of product to the D.B.
@app.post("/api/products")
def create_product():
    #logic Here
    new_product = request.get_json()
    print(new_product)

    name = new_product["name"]
    category = new_product["category"]
    price = new_product["price"]
    image = new_product["image"]


    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO products (name, category, price, image) VALUES (?, ?, ?, ?)", (name, category, price, image))
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "product created successfully"
    }), 201

@app.get("/api/products")
def get_products():

    connection = sqlite3.connect(DB_NAME) # open the connection to the D.B.
    connection.row_factory = sqlite3.Row # makes each row behaves like a dictionary
    cursor = connection.cursor() # execute sql syntax
    cursor.execute("SELECT * FROM products")
    products_db = cursor.fetchall() # retrieves all rows from the result of the query
    connection.close()

    products = []
    for product in products_db:
        products.append(dict(product))

    return jsonify({
        "success": True,
        "message": "products retrieved successfully",
        "data": products
    })


# ----- COUPONS -----
@app.post("/api/coupons")
def create_coupon():
    new_coupon = request.get_json()
    print(new_coupon)

    code = new_coupon["code"]
    discount = new_coupon["discount"]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO coupons(code, discount) VALUES (?, ?)", (code, discount))
    connection.commit()
    connection.close()

    return jsonify({
        "Success": True,
        "message": "coupon added"
    }), 201

init_db()
app.run(debug=True)
