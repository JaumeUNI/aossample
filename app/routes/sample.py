from fastapi import APIRouter, HTTPException
from app.models.item import Item, ArithmeticOperation, OperationUpdate
from typing import List, Dict
from datetime import datetime
import math

router = APIRouter()

# In-memory storage for arithmetic operations
operations_storage: Dict[int, ArithmeticOperation] = {}
operation_counter = 1

# Helper function to calculate arithmetic operations
def calculate_operation(operation: str, value1: float, value2: float) -> float:
    """Calculate arithmetic operation and return result"""
    if operation == "add":
        return value1 + value2
    elif operation == "subtract":
        return value1 - value2
    elif operation == "multiply":
        return value1 * value2
    elif operation == "divide":
        if value2 == 0:
            raise ValueError("Division by zero is not allowed")
        return value1 / value2
    else:
        raise ValueError(f"Unsupported operation: {operation}")

# POST route that accepts JSON data and processes it (original functionality)
@router.post("/process")
def process_data(item: Item):
    try:
        result = item.value1 + item.value2
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# POST route for arithmetic operations (CREATE)
@router.post("/arithmetic", response_model=ArithmeticOperation)
def create_arithmetic_operation(operation_data: ArithmeticOperation):
    """Create a new arithmetic operation"""
    global operation_counter
    try:
        # Calculate the result
        result = calculate_operation(operation_data.operation, operation_data.value1, operation_data.value2)
        
        # Create the operation with ID and timestamp
        new_operation = ArithmeticOperation(
            id=operation_counter,
            operation=operation_data.operation,
            value1=operation_data.value1,
            value2=operation_data.value2,
            result=result,
            timestamp=datetime.now()
        )
        
        # Store in memory
        operations_storage[operation_counter] = new_operation
        operation_counter += 1
        
        return new_operation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# GET route to retrieve all arithmetic operations (READ ALL)
@router.get("/arithmetic", response_model=List[ArithmeticOperation])
def get_all_operations():
    """Get all arithmetic operations"""
    return list(operations_storage.values())

# GET route to retrieve a specific arithmetic operation (READ ONE)
@router.get("/arithmetic/{operation_id}", response_model=ArithmeticOperation)
def get_operation(operation_id: int):
    """Get a specific arithmetic operation by ID"""
    if operation_id not in operations_storage:
        raise HTTPException(status_code=404, detail="Operation not found")
    return operations_storage[operation_id]

# PUT route to completely replace an arithmetic operation (REPLACE)
@router.put("/arithmetic/{operation_id}", response_model=ArithmeticOperation)
def replace_operation(operation_id: int, operation_data: ArithmeticOperation):
    """Replace an existing arithmetic operation completely"""
    if operation_id not in operations_storage:
        raise HTTPException(status_code=404, detail="Operation not found")
    
    try:
        # Calculate the new result
        result = calculate_operation(operation_data.operation, operation_data.value1, operation_data.value2)
        
        # Create new operation with same ID and new timestamp
        updated_operation = ArithmeticOperation(
            id=operation_id,
            operation=operation_data.operation,
            value1=operation_data.value1,
            value2=operation_data.value2,
            result=result,
            timestamp=datetime.now()
        )
        
        # Replace in storage
        operations_storage[operation_id] = updated_operation
        return updated_operation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# PATCH route to partially update an arithmetic operation (UPDATE)
@router.patch("/arithmetic/{operation_id}", response_model=ArithmeticOperation)
def update_operation(operation_id: int, operation_update: OperationUpdate):
    """Partially update an existing arithmetic operation"""
    if operation_id not in operations_storage:
        raise HTTPException(status_code=404, detail="Operation not found")
    
    try:
        # Get existing operation
        existing_operation = operations_storage[operation_id]
        
        # Update only provided fields
        operation = operation_update.operation if operation_update.operation is not None else existing_operation.operation
        value1 = operation_update.value1 if operation_update.value1 is not None else existing_operation.value1
        value2 = operation_update.value2 if operation_update.value2 is not None else existing_operation.value2
        
        # Calculate new result
        result = calculate_operation(operation, value1, value2)
        
        # Create updated operation
        updated_operation = ArithmeticOperation(
            id=operation_id,
            operation=operation,
            value1=value1,
            value2=value2,
            result=result,
            timestamp=datetime.now()
        )
        
        # Update in storage
        operations_storage[operation_id] = updated_operation
        return updated_operation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# DELETE route to remove an arithmetic operation (DELETE)
@router.delete("/arithmetic/{operation_id}")
def delete_operation(operation_id: int):
    """Delete an arithmetic operation"""
    if operation_id not in operations_storage:
        raise HTTPException(status_code=404, detail="Operation not found")
    
    # Remove from storage
    deleted_operation = operations_storage.pop(operation_id)
    return {"message": f"Operation {operation_id} deleted successfully", "deleted_operation": deleted_operation}

# DELETE route to clear all arithmetic operations
@router.delete("/arithmetic")
def delete_all_operations():
    """Delete all arithmetic operations"""
    global operation_counter
    count = len(operations_storage)
    operations_storage.clear()
    operation_counter = 1
    return {"message": f"All {count} operations deleted successfully"}

# GET route to concatenate two strings as query parameters (original functionality)
@router.get("/concat")
def concatenate(param1: str, param2: str):
    return {"result": param1 + param2}

# GET route to return the length of a string as a query parameter (original functionality)
@router.get("/length")
def length_of_string(string: str):
    return {"length": len(string)}
