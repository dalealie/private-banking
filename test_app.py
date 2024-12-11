import pytest
from app import app

@pytest.fixture
def mock_db(mocker):
    # Mock the MySQL connection and cursor
    mock_conn = mocker.patch('flask_mysqldb.MySQL.connection')
    mock_cursor = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock common cursor methods
    mock_cursor.execute.return_value = None  # Ensure execute does nothing
    mock_cursor.fetchall.return_value = []  # Default return for fetchall
    mock_cursor.fetchone.return_value = None  # Default return for fetchone
    mock_cursor.rowcount = 1  # Default rowcount to 1 (for inserts/updates)
    
    return mock_cursor

# Test for the index route
def test_index():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"WELCOME TO PRIVATE BANKING DATABASE" in response.data

# Test for getting employees when the table is empty
def test_get_employees_empty(mock_db):
    mock_db.fetchall.return_value = []  # No employees in the DB

    client = app.test_client()
    response = client.get('/employees')

    assert response.status_code == 404
    assert b"No employees found" in response.data

# Test for getting employees when there are employees
def test_get_employees(mock_db):
    mock_db.fetchall.return_value = [(1, 'John Doe'), (2, 'Jane Smith')]

    client = app.test_client()
    response = client.get('/employees')

    assert response.status_code == 200
    assert b"John Doe" in response.data
    assert b"Jane Smith" in response.data

# Test for adding an employee with missing fields
def test_add_employee_missing_fields(mock_db):
    client = app.test_client()
    response = client.post('/employees', json={})

    assert response.status_code == 400
    assert b"Employee ID and name are required" in response.data

def test_add_employee_success(mock_db):
    # Simulate a successful insertion and retrieval
    mock_db.rowcount = 1  # Simulate successful insert
    mock_db.fetchone.return_value = (1, 'John Doe')  # Simulate employee retrieval after insertion

    client = app.test_client()
    response = client.post('/employees', json={'employee_ID': 1, 'name': 'John Doe'})

    assert response.status_code == 201
    assert b"employee_ID" in response.data
    assert b"1" in response.data  # Check for employee ID
    assert b"John Doe" in response.data  # Check for employee name
    
# Test for updating an employee with missing fields
def test_update_employee_missing_fields(mock_db):
    client = app.test_client()
    response = client.put('/employees/1', json={})

    assert response.status_code == 400
    assert b"Name is required" in response.data

# Test for trying to update an employee that doesn't exist
def test_update_employee_not_found(mock_db):
    mock_db.rowcount = 0  # Simulate no employee found

    client = app.test_client()
    response = client.put('/employees/999', json={'name': 'Updated Name'})

    assert response.status_code == 404
    assert b"Employee not found" in response.data

# Test for deleting an employee that doesn't exist
def test_delete_employee_not_found(mock_db):
    mock_db.rowcount = 0  # Simulate no employee found

    client = app.test_client()
    response = client.delete('/employees/999')

    assert response.status_code == 404
    assert b"Employee not found" in response.data

def test_delete_employee_success(mock_db):
    # Simulate that the employee exists before deletion
    mock_db.fetchone.return_value = (1, 'John Doe')  # Simulate employee found
    mock_db.rowcount = 1  # Simulate successful deletion

    client = app.test_client()
    response = client.delete('/employees/1')

    assert response.status_code == 200
    assert b"Employee with ID 1 has been deleted." in response.data  # Success message