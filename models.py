from pydantic import BaseModel, Field
from typing import Optional

class ItemCreate(BaseModel):
    """Model for creating a new item"""
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 1

class ItemUpdate(BaseModel):
    """Model for updating an item (all fields optional)"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

class Item(BaseModel):
    """Model for item response"""
    id: str = Field(alias="_id")
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 1

    class Config:
        populate_by_name = True

class HealthResponse(BaseModel):
    """Model for health check response"""
    status: str
    message: str
