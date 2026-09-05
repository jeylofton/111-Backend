from flask import Flask, jsonify
import sqlite3

app = Flask(__name__) # Instance of Flask


DB_NAME = "online-store.db"

def init_db():
    connection = sqlite3.connect(DB_NAME) # Opens the connection to the D.B. files named 'online-store.db'
    cursor = connection.cursor() # Creates a cursor/tool that lets us send commands (Select/Insert,...) to the D.B.



@app.get("/api/health")
def health_check():
    return jsonify({"status": "Ok"}), 200


app.run(debug=True)