# FastAPI Sample Project for Render

A minimal FastAPI project ready for deployment on Render cloud platform.

## Features

- ✅ Simple CRUD API for items
- ✅ Health check endpoints
- ✅ CORS enabled
- ✅ Pydantic models for validation
- ✅ Ready for Render deployment

## API Endpoints

- `GET /` - Root endpoint (health check)
- `GET /health` - Health check endpoint
- `POST /items/{item_id}` - Create a new item
- `GET /items/{item_id}` - Get item by ID
- `GET /items` - List all items
- `DELETE /items/{item_id}` - Delete an item

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

Access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deploying to Render

### Method 1: Using render.yaml (Recommended)

1. Push this project to a GitHub repository
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` and deploy your app

### Method 2: Manual Deployment

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `fastapi-sample` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`

5. Click "Create Web Service"

Your API will be live at `https://your-app-name.onrender.com`

## Testing the API

### Using curl

```bash
# Health check
curl https://your-app-name.onrender.com/health

# Create an item
curl -X POST "https://your-app-name.onrender.com/items/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "A test item", "price": 29.99, "quantity": 5}'

# Get an item
curl https://your-app-name.onrender.com/items/1

# List all items
curl https://your-app-name.onrender.com/items
```

### Using the Interactive Docs

Visit `https://your-app-name.onrender.com/docs` to use the Swagger UI for testing.

## Project Structure

```
.
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── render.yaml         # Render deployment configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Notes

- The free tier on Render may spin down after inactivity. The first request after inactivity might take 30-60 seconds.
- This project uses in-memory storage, so data will be lost when the service restarts.
- For production, consider adding a database (PostgreSQL, MongoDB, etc.)

## Next Steps

To enhance this project, consider:
- Adding a database (PostgreSQL with SQLAlchemy)
- Implementing authentication (JWT tokens)
- Adding more comprehensive error handling
- Setting up logging
- Adding unit tests
- Implementing rate limiting

## License

MIT
