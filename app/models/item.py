from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    value1: int
    value2: int

class ArithmeticOperation(BaseModel):
    id: Optional[int] = None
    operation: str  # "add", "subtract", "multiply", "divide"
    value1: float
    value2: float
    result: Optional[float] = None
    timestamp: Optional[datetime] = None

class OperationUpdate(BaseModel):
    operation: Optional[str] = None
    value1: Optional[float] = None
    value2: Optional[float] = None
