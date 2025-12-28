# FastAPI MongoDB CRUD Application

A simple and clean CRUD (Create, Read, Update, Delete) application built with FastAPI and MongoDB, ready for deployment on Render.

## Features

- ✅ Full CRUD operations for items
- ✅ MongoDB Atlas integration
- ✅ Environment-based configuration
- ✅ Async/await for better performance
- ✅ CORS enabled for frontend access
- ✅ Ready for Render deployment
- ✅ Comprehensive error handling

## Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **Motor** - Async MongoDB driver for Python
- **MongoDB Atlas** - Cloud-hosted MongoDB (free tier)
- **Pydantic** - Data validation
- **Python-dotenv** - Environment variable management

## Prerequisites

- Python 3.12+
- MongoDB Atlas account (free tier)
- Git (for deployment)

## MongoDB Atlas Setup

1. **Create a free MongoDB Atlas account** at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)

2. **Create a cluster** (free M0 tier)

3. **Create a database user**:
   - Go to Database Access
   - Add a new user with username and password
   - Remember these credentials!

4. **Whitelist your IP**:
   - Go to Network Access
   - Add IP Address → Allow Access from Anywhere (0.0.0.0/0) for development

5. **Get your connection string**:
   - Go to your cluster → Connect → Connect your application
   - Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/...`)
   - Replace `<password>` with your actual password

## Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd test
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file**:
   ```bash
   # Copy the example file
   cp .env.example .env
   ```

4. **Edit `.env` file** with your MongoDB connection string:
   ```env
   MONGODB_URL=mongodb+srv://your_username:your_password@cluster.mongodb.net/?retryWrites=true&w=majority
   DATABASE_NAME=crud_app
   PORT=8000
   ENVIRONMENT=development
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

6. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Root health check
- `GET /health` - Detailed health check with MongoDB status

### CRUD Operations

#### Create Item
```http
POST /items
Content-Type: application/json

{
  "name": "Laptop",
  "description": "MacBook Pro 14-inch",
  "price": 1999.99,
  "quantity": 5
}
```

#### Get All Items
```http
GET /items
```

#### Get Single Item
```http
GET /items/{item_id}
```

#### Update Item
```http
PUT /items/{item_id}
Content-Type: application/json

{
  "price": 1899.99,
  "quantity": 3
}
```

#### Delete Item
```http
DELETE /items/{item_id}
```

## Deployment to Render

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "MongoDB CRUD application"
   git push origin main
   ```

2. **Create a new Web Service on Render**:
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure environment variables** in Render dashboard:
   - `MONGODB_URL` - Your MongoDB Atlas connection string (set as secret)
   - `DATABASE_NAME` - `crud_app`
   - `ENVIRONMENT` - `production`

4. **Deploy**:
   - Render will automatically build and deploy using `render.yaml`
   - Your API will be available at: `https://your-service.onrender.com`

## Project Structure

```
test/
├── main.py              # FastAPI application with CRUD endpoints
├── database.py          # MongoDB connection and configuration
├── models.py            # Pydantic models for data validation
├── requirements.txt     # Python dependencies
├── render.yaml          # Render deployment configuration
├── .env.example         # Environment variables template
├── .env                 # Your local environment variables (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Example Usage with cURL

```bash
# Create an item
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","description":"MacBook Pro","price":1999.99,"quantity":5}'

# Get all items
curl "http://localhost:8000/items"

# Get specific item (replace with actual ID)
curl "http://localhost:8000/items/65a1b2c3d4e5f6g7h8i9j0k1"

# Update item
curl -X PUT "http://localhost:8000/items/65a1b2c3d4e5f6g7h8i9j0k1" \
  -H "Content-Type: application/json" \
  -d '{"price":1899.99}'

# Delete item
curl -X DELETE "http://localhost:8000/items/65a1b2c3d4e5f6g7h8i9j0k1"
```

## Development Notes

- The application uses Motor for async MongoDB operations
- All endpoints use proper HTTP status codes
- Error handling is implemented for common scenarios
- CORS is enabled for all origins (configure for production use)
- MongoDB ObjectIds are used as item identifiers

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017` | Yes |
| `DATABASE_NAME` | Database name | `crud_app` | No |
| `PORT` | Server port | `8000` | No |
| `ENVIRONMENT` | Environment mode | `development` | No |

## License

MIT

## Support

For issues or questions, please open an issue on GitHub.
