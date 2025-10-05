# AI Copilot Web Application - Backend Service

## Overview
This is the backend service for the AI Copilot web application. It handles frontend requests, communicates with the Gemini API for AI responses, and manages chat flows.

## Project Structure
```
backend_service/
├── src/
│   └── api/
│       ├── __init__.py
│       ├── main.py              # FastAPI application entry point
│       └── generate_openapi.py  # OpenAPI schema generator
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
- `GEMINI_API_KEY`: Your Gemini API key for AI chat functionality

### 2. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Server
```bash
source venv/bin/activate
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

### 4. Access API Documentation
Once running, visit:
- Swagger UI: http://localhost:3001/docs
- ReDoc: http://localhost:3001/redoc
- OpenAPI JSON: http://localhost:3001/openapi.json

## API Endpoints

### Health Check
- **GET** `/` - Returns service health status

### Future Endpoints (to be implemented)
- **POST** `/chat` - Send message to AI and get response
- **GET** `/history` - Retrieve chat conversation history

## Development

### Generate OpenAPI Schema
```bash
python -m src.api.generate_openapi
```

### Run Tests
```bash
pytest
```

### Linting
```bash
./../.init/.linter.sh
```

## Technology Stack
- **Framework**: FastAPI
- **ASGI Server**: Uvicorn
- **API Documentation**: OpenAPI 3.1.0 with Swagger UI
- **CORS**: Enabled for frontend communication
- **AI Integration**: Google Gemini API

## Environment Variables
See `.env.example` for all required and optional environment variables.

## Notes
- CORS is configured to allow requests from the frontend application
- API keys should never be committed to version control
- The service runs on port 3001 by default
