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

    # Mini Challenge
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
    cursor.execute("INSERT INTO products (name, catagory, price, image) VALUE (?, ?, ?, ?)", (name, category, price, image))
    cursor.commit()
    cursor.close()

    return jsonify({
        "success": True,
        "message": "product created successfully"
    }), 201

# ----- COUPONS -----


init_db()
app.run(debug=True)
