from flask import Flask, request, jsonify

app = Flask(__name__)

employees = []

@app.route("/")
def home():
    return "Employee API Running"

# CREATE
@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.json

    employee = {
        "id": data["id"],
        "name": data["name"],
        "salary": data["salary"]
    }

    employees.append(employee)
    return jsonify({"message": "Employee Added"})

# READ ALL
@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)

# READ ONE
@app.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):
    for e in employees:
        if e["id"] == id:
            return jsonify(e)
    return jsonify({"message": "Not Found"})

# DELETE
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    global employees
    employees = [e for e in employees if e["id"] != id]
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    app.run(debug=True)