from flask import Flask, request, jsonify, abort
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "mini_private_banking"  # Replace with your database name
mysql = MySQL(app)

# Error handler
def handle_error(error_msg, status_code):
    return jsonify({"error": error_msg}), status_code

# Index Route
@app.route("/")
def hello_world():
    return "WELCOME TO PRIVATE BANKING DATABASE"

# --- GET Routes ---

# GET Employees
@app.route("/employees")
def get_employees():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()
    if not employees:
        return handle_error("No employees found", 404)
    
    employees_list = [
        {
            "employee_ID": employee[0], 
            "name": employee[1]
        }
        for employee in employees
    ]
    
    return jsonify(employees_list), 200

# GET Clients
@app.route("/clients")
def get_clients():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Clients")
    clients = cursor.fetchall()
    if not clients:
        return handle_error("No clients found", 404)

    clients_list = [
        {
            "client_ID": client[0], 
            "name": client[1], 
            "email": client[2], 
            "phone": client[3],
            "client_Manager_Employee_ID": client[4]
        }
        for client in clients
    ]
    
    return jsonify(clients_list), 200

# GET Products
@app.route("/products")
def get_products():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    if not products:
        return handle_error("No products found", 404)

    products_list = [
        {
            "product_ID": product[0], 
            "product_Type": product[1]
        }
        for product in products
    ]
    
    return jsonify(products_list), 200

# GET Transactions
@app.route("/transactions")
def get_transactions():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Transactions")
    transactions = cursor.fetchall()
    if not transactions:
        return handle_error("No transactions found", 404)

    transactions_list = [
        {
            "transaction_ID": transaction[0],
            "client_ID": transaction[1], 
            "product_ID": transaction[2], 
            "transaction_Amount": transaction[3], 
            "transaction_Date": transaction[4]
        }
        for transaction in transactions
    ]
    
    return jsonify(transactions_list), 200

# --- POST Routes ---

# POST Employees
@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json()
    employee_id = data.get('employee_ID')
    name = data.get('name')
    
    if not employee_id or not name:
        return handle_error("Employee ID and name are required", 400)
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Employees (Employee_ID, Name) VALUES (%s, %s)", (employee_id, name))
    mysql.connection.commit()

    # Fetch the newly added employee to return the added data
    cursor.execute("SELECT * FROM Employees WHERE Employee_ID = %s", (employee_id,))
    employee = cursor.fetchone()

    if not employee:
        return handle_error("Failed to retrieve the added employee", 500)

    return jsonify({
        "employee_ID": employee[0], 
        "name": employee[1]
    }), 201

# POST Clients
@app.route("/clients", methods=["POST"])
def add_client():
    data = request.get_json()
    client_id = data.get('client_ID')
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    client_manager_employee_id = data.get('client_Manager_Employee_ID')

    if not all([client_id, name, email, phone, client_manager_employee_id]):
        return handle_error("Missing required fields", 400)
    
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Clients (Client_ID, Name, Email, Phone, Client_Manager_Employee_ID) VALUES (%s, %s, %s, %s, %s)", 
        (client_id, name, email, phone, client_manager_employee_id)
    )
    mysql.connection.commit()

    # Fetch the newly added client
    cursor.execute("SELECT * FROM Clients WHERE Client_ID = %s", (client_id,))
    client = cursor.fetchone()

    if not client:
        return handle_error("Failed to retrieve the added client", 500)

    return jsonify({
        "client_ID": client[0], 
        "name": client[1], 
        "email": client[2], 
        "phone": client[3],
        "client_Manager_Employee_ID": client[4]
    }), 201

# POST Products
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    product_id = data.get('product_ID')
    product_type = data.get('product_Type')

    if not all([product_id, product_type]):
        return handle_error("Missing required fields", 400)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Products (Product_ID, Product_Type) VALUES (%s, %s)", 
        (product_id, product_type)
    )
    mysql.connection.commit()

    # Fetch the newly added product
    cursor.execute("SELECT * FROM Products WHERE Product_ID = %s", (product_id,))
    product = cursor.fetchone()

    if not product:
        return handle_error("Failed to retrieve the added product", 500)

    return jsonify({
        "product_ID": product[0], 
        "product_Type": product[1]
    }), 201

# POST Transactions
@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    transaction_id = data.get('transaction_ID')
    client_id = data.get('client_ID')
    product_id = data.get('product_ID')
    transaction_amount = data.get('transaction_Amount')
    transaction_date = data.get('transaction_Date')

    if not all([transaction_id, client_id, product_id, transaction_amount, transaction_date]):
        return handle_error("Missing required fields", 400)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Transactions (Transaction_ID, Client_ID, Product_ID, Transaction_Amount, Transaction_Date) VALUES (%s, %s, %s, %s, %s)",
        (transaction_id, client_id, product_id, transaction_amount, transaction_date)
    )
    mysql.connection.commit()

    # Fetch the newly added transaction
    cursor.execute("SELECT * FROM Transactions WHERE Transaction_ID = %s", (transaction_id,))
    transaction = cursor.fetchone()

    if not transaction:
        return handle_error("Failed to retrieve the added transaction", 500)

    return jsonify({
        "transaction_ID": transaction[0], 
        "client_ID": transaction[1], 
        "product_ID": transaction[2], 
        "transaction_Amount": transaction[3], 
        "transaction_Date": transaction[4]
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
