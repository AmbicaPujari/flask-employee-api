from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = "employees.db"

# ----------------------------
# DATABASE SETUP
# ----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------------------
# HOME
# ----------------------------
@app.route("/")
def home():
    return "Employee API Running"

# ----------------------------
# CREATE EMPLOYEE
# ----------------------------
@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.json

    if not data or "id" not in data or "name" not in data or "salary" not in data:
        return jsonify({"error": "Invalid input"}), 400

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO employees (id, name, salary) VALUES (?, ?, ?)",
            (data["id"], data["name"], data["salary"])
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "Employee added successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Employee ID already exists"}), 409

# ----------------------------
# GET ALL EMPLOYEES
# ----------------------------
@app.route("/employees", methods=["GET"])
def get_employees():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()

    employees = [
        {"id": row[0], "name": row[1], "salary": row[2]}
        for row in rows
    ]

    return jsonify(employees), 200

# ----------------------------
# GET ONE EMPLOYEE
# ----------------------------
@app.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({"id": row[0], "name": row[1], "salary": row[2]}), 200

    return jsonify({"error": "Employee not found"}), 404

# ----------------------------
# DELETE EMPLOYEE
# ----------------------------
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM employees WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Employee deleted"}), 200

# ----------------------------
# RUN APP
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
