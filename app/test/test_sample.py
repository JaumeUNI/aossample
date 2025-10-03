from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ========== ORIGINAL FUNCTIONALITY TESTS ==========

# Test for POST /process
def test_process_data():
    response = client.post("/process", json={"value1": 10, "value2": 5})
    assert response.status_code == 200
    assert response.json() == {"result": 15}

# Test for POST /process with invalid data
def test_process_data_invalid():
    response = client.post("/process", json={"value1": 10})
    assert response.status_code == 422

# Test for GET /concat
def test_concatenate():
    response = client.get("/concat?param1=Hello&param2=World")
    assert response.status_code == 200
    assert response.json() == {"result": "HelloWorld"}

# Test for GET /length
def test_length_of_string():
    response = client.get("/length?string=FastAPI")
    assert response.status_code == 200
    assert response.json() == {"length": 7}

# ========== ARITHMETIC OPERATIONS CRUD TESTS ==========

# CREATE Tests (POST)
def test_create_addition():
    """Test creating an addition operation"""
    response = client.post("/arithmetic", json={
        "operation": "add",
        "value1": 10.0,
        "value2": 5.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "add"
    assert data["value1"] == 10.0
    assert data["value2"] == 5.0
    assert data["result"] == 15.0
    assert data["id"] == 1
    assert "timestamp" in data

def test_create_subtraction():
    """Test creating a subtraction operation"""
    response = client.post("/arithmetic", json={
        "operation": "subtract",
        "value1": 10.0,
        "value2": 3.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 7.0

def test_create_multiplication():
    """Test creating a multiplication operation"""
    response = client.post("/arithmetic", json={
        "operation": "multiply",
        "value1": 4.0,
        "value2": 5.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 20.0

def test_create_division():
    """Test creating a division operation"""
    response = client.post("/arithmetic", json={
        "operation": "divide",
        "value1": 15.0,
        "value2": 3.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 5.0

def test_create_division_by_zero():
    """Test division by zero error"""
    response = client.post("/arithmetic", json={
        "operation": "divide",
        "value1": 10.0,
        "value2": 0.0
    })
    assert response.status_code == 400
    assert "Division by zero" in response.json()["detail"]

def test_create_invalid_operation():
    """Test invalid operation type"""
    response = client.post("/arithmetic", json={
        "operation": "invalid",
        "value1": 10.0,
        "value2": 5.0
    })
    assert response.status_code == 400
    assert "Unsupported operation" in response.json()["detail"]

# READ Tests (GET)
def test_get_all_operations():
    """Test retrieving all operations"""
    # Clear storage first
    client.delete("/arithmetic")
    
    # Create some operations
    client.post("/arithmetic", json={"operation": "add", "value1": 1.0, "value2": 2.0})
    client.post("/arithmetic", json={"operation": "multiply", "value1": 3.0, "value2": 4.0})
    
    response = client.get("/arithmetic")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["operation"] == "add"
    assert data[1]["operation"] == "multiply"

def test_get_specific_operation():
    """Test retrieving a specific operation"""
    # Create an operation
    create_response = client.post("/arithmetic", json={
        "operation": "add",
        "value1": 10.0,
        "value2": 20.0
    })
    operation_id = create_response.json()["id"]
    
    # Get the specific operation
    response = client.get(f"/arithmetic/{operation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == operation_id
    assert data["result"] == 30.0

def test_get_nonexistent_operation():
    """Test retrieving a non-existent operation"""
    response = client.get("/arithmetic/999")
    assert response.status_code == 404
    assert "Operation not found" in response.json()["detail"]

# UPDATE Tests (PUT - Replace)
def test_replace_operation():
    """Test completely replacing an operation"""
    # Create an operation
    create_response = client.post("/arithmetic", json={
        "operation": "add",
        "value1": 5.0,
        "value2": 5.0
    })
    operation_id = create_response.json()["id"]
    
    # Replace the operation
    response = client.put(f"/arithmetic/{operation_id}", json={
        "operation": "multiply",
        "value1": 3.0,
        "value2": 7.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "multiply"
    assert data["value1"] == 3.0
    assert data["value2"] == 7.0
    assert data["result"] == 21.0
    assert data["id"] == operation_id

def test_replace_nonexistent_operation():
    """Test replacing a non-existent operation"""
    response = client.put("/arithmetic/999", json={
        "operation": "add",
        "value1": 1.0,
        "value2": 1.0
    })
    assert response.status_code == 404
    assert "Operation not found" in response.json()["detail"]

# UPDATE Tests (PATCH - Partial Update)
def test_partial_update_operation():
    """Test partially updating an operation"""
    # Create an operation
    create_response = client.post("/arithmetic", json={
        "operation": "add",
        "value1": 10.0,
        "value2": 5.0
    })
    operation_id = create_response.json()["id"]
    
    # Partially update the operation
    response = client.patch(f"/arithmetic/{operation_id}", json={
        "operation": "multiply",
        "value1": 2.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "multiply"
    assert data["value1"] == 2.0
    assert data["value2"] == 5.0  # Should remain unchanged
    assert data["result"] == 10.0

def test_partial_update_nonexistent_operation():
    """Test partially updating a non-existent operation"""
    response = client.patch("/arithmetic/999", json={"operation": "multiply"})
    assert response.status_code == 404
    assert "Operation not found" in response.json()["detail"]

# DELETE Tests
def test_delete_specific_operation():
    """Test deleting a specific operation"""
    # Create an operation
    create_response = client.post("/arithmetic", json={
        "operation": "add",
        "value1": 1.0,
        "value2": 1.0
    })
    operation_id = create_response.json()["id"]
    
    # Delete the operation
    response = client.delete(f"/arithmetic/{operation_id}")
    assert response.status_code == 200
    data = response.json()
    assert "deleted successfully" in data["message"]
    assert data["deleted_operation"]["id"] == operation_id
    
    # Verify it's deleted
    get_response = client.get(f"/arithmetic/{operation_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_operation():
    """Test deleting a non-existent operation"""
    response = client.delete("/arithmetic/999")
    assert response.status_code == 404
    assert "Operation not found" in response.json()["detail"]

def test_delete_all_operations():
    """Test deleting all operations"""
    # Clear any existing operations first
    client.delete("/arithmetic")
    
    # Create some operations
    client.post("/arithmetic", json={"operation": "add", "value1": 1.0, "value2": 1.0})
    client.post("/arithmetic", json={"operation": "multiply", "value1": 2.0, "value2": 2.0})
    
    # Delete all operations
    response = client.delete("/arithmetic")
    assert response.status_code == 200
    data = response.json()
    assert "All 2 operations deleted successfully" in data["message"]
    
    # Verify all are deleted
    get_response = client.get("/arithmetic")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0

