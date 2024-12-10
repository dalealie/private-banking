from flask import Flask, request, jsonify, abort
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "private_banking"  # Replace with your database name
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
            "employee_ID": employee[0]
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
            "address_ID": client[1], 
            "bank_ID": client[2],
            "client_Manager_Employee_ID": client[3]
        }
        for client in clients
    ]
    
    return jsonify(clients_list), 200

# GET Cash Flows
@app.route("/cash_flows")
def get_cash_flows():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Cash_Flows")
    cash_flows = cursor.fetchall()
    if not cash_flows:
        return handle_error("No cash flows found", 404)

    cash_flows_list = [
        {
            "cash_Flow_ID": cash_flow[0], 
            "client_ID": cash_flow[1]
        }
        for cash_flow in cash_flows
    ]
    
    return jsonify(cash_flows_list), 200

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
            "product_Type_Code": product[1]
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
            "contact_ID": transaction[2], 
            "employee_ID": transaction[3], 
            "partner_ID": transaction[4], 
            "product_ID": transaction[5], 
            "stock_Symbol": transaction[6], 
            "transaction_Date": transaction[7], 
            "transaction_Type_Code": transaction[8]
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
    
    if not employee_id:
        return handle_error("Employee ID is required", 400)
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Employees (Employee_ID) VALUES (%s)", (employee_id,))
    mysql.connection.commit()
    
    # Fetch the newly added employee to return the added data
    cursor.execute("SELECT * FROM Employees WHERE Employee_ID = %s", (employee_id,))
    employee = cursor.fetchone()

    return jsonify({
        "employee_ID": employee[0]
    }), 201

# POST Clients
@app.route("/clients", methods=["POST"])
def add_client():
    data = request.get_json()
    client_id = data.get('client_ID')
    address_id = data.get('address_ID')
    bank_id = data.get('bank_ID')
    client_manager_employee_id = data.get('client_Manager_Employee_ID')

    if not all([client_id, address_id, bank_id, client_manager_employee_id]):
        return handle_error("Missing required fields", 400)
    
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Clients (Client_ID, Address_ID, Bank_ID, Client_Manager_Employee_ID) VALUES (%s, %s, %s, %s)", 
        (client_id, address_id, bank_id, client_manager_employee_id)
    )
    mysql.connection.commit()

    # Fetch the newly added client
    cursor.execute("SELECT * FROM Clients WHERE Client_ID = %s", (client_id,))
    client = cursor.fetchone()

    return jsonify({
        "client_ID": client[0], 
        "address_ID": client[1], 
        "bank_ID": client[2],
        "client_Manager_Employee_ID": client[3]
    }), 201

# POST Cash Flows
@app.route("/cash_flows", methods=["POST"])
def add_cash_flow():
    data = request.get_json()
    cash_flow_id = data.get('cash_Flow_ID')
    client_id = data.get('client_ID')

    if not cash_flow_id or not client_id:
        return handle_error("Missing required fields", 400)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Cash_Flows (Cash_Flow_ID, Client_ID) VALUES (%s, %s)", 
        (cash_flow_id, client_id)
    )
    mysql.connection.commit()

    # Fetch the newly added cash flow
    cursor.execute("SELECT * FROM Cash_Flows WHERE Cash_Flow_ID = %s", (cash_flow_id,))
    cash_flow = cursor.fetchone()

    return jsonify({
        "cash_Flow_ID": cash_flow[0], 
        "client_ID": cash_flow[1]
    }), 201

# POST Products
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    product_id = data.get('product_ID')
    product_type_code = data.get('product_Type_Code')

    if not all([product_id, product_type_code]):
        return handle_error("Missing required fields", 400)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Products (Product_ID, Product_Type_Code) VALUES (%s, %s)", 
        (product_id, product_type_code)
    )
    mysql.connection.commit()

    # Fetch the newly added product
    cursor.execute("SELECT * FROM Products WHERE Product_ID = %s", (product_id,))
    product = cursor.fetchone()

    return jsonify({
        "product_ID": product[0], 
        "product_Type_Code": product[1]
    }), 201

# POST Transactions
@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    transaction_id = data.get('transaction_ID')
    client_id = data.get('client_ID')
    contact_id = data.get('contact_ID')
    employee_id = data.get('employee_ID')
    partner_id = data.get('partner_ID')
    product_id = data.get('product_ID')
    stock_symbol = data.get('stock_Symbol')
    transaction_date = data.get('transaction_Date')
    transaction_type_code = data.get('transaction_Type_Code')

    if not all([transaction_id, client_id, contact_id, employee_id, partner_id, product_id, stock_symbol, transaction_date, transaction_type_code]):
        return handle_error("Missing required fields", 400)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Transactions (Transaction_ID, Client_ID, Contact_ID, Employee_ID, Partner_ID, Product_ID, Stock_Symbol, Transaction_Date, Transaction_Type_Code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (transaction_id, client_id, contact_id, employee_id, partner_id, product_id, stock_symbol, transaction_date, transaction_type_code)
    )
    mysql.connection.commit()

    # Fetch the newly added transaction
    cursor.execute("SELECT * FROM Transactions WHERE Transaction_ID = %s", (transaction_id,))
    transaction = cursor.fetchone()

    return jsonify({
        "transaction_ID": transaction[0], 
        "client_ID": transaction[1], 
        "contact_ID": transaction[2], 
        "employee_ID": transaction[3], 
        "partner_ID": transaction[4], 
        "product_ID": transaction[5], 
        "stock_Symbol": transaction[6], 
        "transaction_Date": transaction[7], 
        "transaction_Type_Code": transaction[8]
    }), 201

if __name__ == "__main__":
    app.run(debug=True)
