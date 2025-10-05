# AI Copilot Web Application - Backend Service

## Overview
This is the backend service for the AI Copilot web application. It handles frontend requests, communicates with the Gemini API for AI responses, and manages chat flows.

## Project Structure
```
backend_service/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   └── generate_openapi.py  # OpenAPI schema generator
│   ├── models/
│   │   ├── __init__.py
│   │   └── chat.py              # Pydantic models for chat endpoints
│   └── services/
│       ├── __init__.py
│       ├── gemini_service.py    # Gemini API integration
│       └── storage_service.py   # In-memory conversation storage
├── interfaces/
│   └── openapi.json            # Generated OpenAPI specification
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .env.example               # Example environment variables
└── .gitignore                 # Git ignore rules
```

## Setup Instructions

### 1. Environment Setup
Copy `.env.example` to `.env` and configure your environment variables:
```bash
cp .env.example .env
```

Required environment variables:
- `GEMINI_API_KEY`: Your Gemini API key for AI chat functionality (get it from https://makersuite.google.com/app/apikey)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins (use `*` for development)

### 2. Install Dependencies
```bash
cd backend_service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Server
```bash
source venv/bin/activate
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

The server will start on http://localhost:3001

### 4. Access API Documentation
Once running, visit:
- Swagger UI: http://localhost:3001/docs
- ReDoc: http://localhost:3001/redoc
- OpenAPI JSON: http://localhost:3001/openapi.json

## API Endpoints

### Health Check
- **GET** `/` - Returns service health status
- **GET** `/health` - Returns detailed health information

### Chat
- **POST** `/chat` - Send message to AI and get response
  - Request body: `{"message": "your message", "conversation_id": "optional-uuid"}`
  - Response: `{"response": "AI response", "conversation_id": "uuid", "timestamp": "ISO datetime"}`

- **GET** `/history?conversation_id=<uuid>` - Retrieve chat conversation history
  - Query parameter: `conversation_id` (required)
  - Response: `{"conversation_id": "uuid", "messages": [...]}`

- **GET** `/conversations` - List all conversation IDs
  - Response: `{"conversations": ["uuid1", "uuid2", ...], "count": 2}`

## Features

### Gemini API Integration
- Integrates with Google Gemini API for AI-powered responses
- Graceful fallback to mock responses when API key is not configured
- Conversation context included in API calls (last 5 messages)

### CORS Configuration
- Configurable via `ALLOWED_ORIGINS` environment variable
- Supports multiple origins (comma-separated)
- Credentials support enabled

### In-Memory Storage
- Current implementation uses in-memory dictionary for conversation storage
- **TODO**: Replace with persistent database (PostgreSQL, MongoDB, etc.)
- Suitable for development and testing only

### Error Handling
- Comprehensive error handling with appropriate HTTP status codes
- Detailed logging for debugging
- User-friendly error messages

## Development

### Generate OpenAPI Schema
```bash
python -m src.api.generate_openapi
```

This will generate/update the `interfaces/openapi.json` file.

### Run Tests
```bash
pytest
```

### Linting
```bash
./../.init/.linter.sh
```

## Technology Stack
- **Framework**: FastAPI 0.115.12
- **ASGI Server**: Uvicorn
- **API Documentation**: OpenAPI 3.1.0 with Swagger UI
- **CORS**: Enabled for frontend communication
- **AI Integration**: Google Gemini API (google-generativeai 0.8.3)
- **Data Validation**: Pydantic 2.11.3

## Environment Variables
See `.env.example` for all required and optional environment variables:
- `GEMINI_API_KEY` - Your Gemini API key (required for AI responses)
- `ALLOWED_ORIGINS` - CORS allowed origins (default: `*`)

## Notes
- CORS is configured to allow requests from the frontend application
- API keys should never be committed to version control
- The service runs on port 3001 by default
- Mock responses are provided when Gemini API is not configured
- Conversation history is currently stored in-memory and will be lost on restart

## Deployment Considerations
- Set `ALLOWED_ORIGINS` to specific frontend URL(s) in production
- Use environment-specific `.env` files
- Implement persistent database storage for conversations
- Add rate limiting for API endpoints
- Enable HTTPS in production
- Add authentication/authorization as needed
