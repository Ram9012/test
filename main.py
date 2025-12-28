from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from bson import ObjectId
from typing import List
import uvicorn
import os
from dotenv import load_dotenv

from database import connect_to_mongo, close_mongo_connection, get_database
from models import Item, ItemCreate, ItemUpdate, HealthResponse

# Load environment variables
load_dotenv()

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB
    await connect_to_mongo()
    yield
    # Shutdown: Close MongoDB connection
    await close_mongo_connection()

# Initialize FastAPI app
app = FastAPI(
    title="MongoDB CRUD API",
    description="A simple CRUD application with MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to convert MongoDB document to Item
def item_helper(item) -> dict:
    return {
        "_id": str(item["_id"]),
        "name": item["name"],
        "description": item.get("description"),
        "price": item["price"],
        "quantity": item["quantity"]
    }

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return {
        "status": "healthy",
        "message": "MongoDB CRUD API is running!"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    db = get_database()
    try:
        # Ping database to check connection
        await db.command("ping")
        return {
            "status": "healthy",
            "message": "All systems operational - MongoDB connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """Create a new item"""
    db = get_database()
    item_dict = item.model_dump()
    
    try:
        result = await db.items.insert_one(item_dict)
        created_item = await db.items.find_one({"_id": result.inserted_id})
        return item_helper(created_item)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating item: {str(e)}"
        )

@app.get("/items", response_model=List[Item])
async def get_all_items():
    """Get all items"""
    db = get_database()
    
    try:
        items = []
        async for item in db.items.find():
            items.append(item_helper(item))
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching items: {str(e)}"
        )

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    """Get a single item by ID"""
    db = get_database()
    
    # Validate ObjectId
    if not ObjectId.is_valid(item_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid item ID format"
        )
    
    try:
        item = await db.items.find_one({"_id": ObjectId(item_id)})
        if item:
            return item_helper(item)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching item: {str(e)}"
        )

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: ItemUpdate):
    """Update an item"""
    db = get_database()
    
    # Validate ObjectId
    if not ObjectId.is_valid(item_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid item ID format"
        )
    
    # Only update fields that are provided
    update_data = {k: v for k, v in item.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    try:
        result = await db.items.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
        
        updated_item = await db.items.find_one({"_id": ObjectId(item_id)})
        return item_helper(updated_item)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating item: {str(e)}"
        )

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    """Delete an item"""
    db = get_database()
    
    # Validate ObjectId
    if not ObjectId.is_valid(item_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid item ID format"
        )
    
    try:
        result = await db.items.delete_one({"_id": ObjectId(item_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
        
        return {
            "message": f"Item {item_id} deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting item: {str(e)}"
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
