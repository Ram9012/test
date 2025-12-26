from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(
    title="Sample FastAPI Project",
    description="A minimal FastAPI project for Render deployment",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 1

class HealthResponse(BaseModel):
    status: str
    message: str

# In-memory storage (for demo purposes)
items_db = {}

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return {
        "status": "healthy",
        "message": "FastAPI server is running on Render!"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "All systems operational"
    }

@app.post("/items/{item_id}", response_model=Item)
async def create_item(item_id: int, item: Item):
    """Create a new item"""
    items_db[item_id] = item
    return item

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get an item by ID"""
    if item_id not in items_db:
        return {"error": "Item not found"}
    return items_db[item_id]

@app.get("/items")
async def list_items():
    """List all items"""
    return {
        "count": len(items_db),
        "items": items_db
    }

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item"""
    if item_id in items_db:
        del items_db[item_id]
        return {"message": f"Item {item_id} deleted successfully"}
    return {"error": "Item not found"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
