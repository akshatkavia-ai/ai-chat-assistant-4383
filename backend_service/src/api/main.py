import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import logging

from src.models.chat import ChatRequest, ChatResponse, ConversationHistory, Message
from src.services.gemini_service import GeminiService
from src.services.storage_service import StorageService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize services
gemini_service = GeminiService()
storage_service = StorageService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    logger.info("Starting AI Copilot Backend Service")
    
    # Log Gemini API key status on startup
    gemini_key_present = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_GEMINI_API_KEY"))
    logger.info(f"Gemini API key present: {'yes' if gemini_key_present else 'no'}")
    
    if gemini_key_present:
        if gemini_service.model:
            logger.info("Gemini API service: ACTIVE (real API responses enabled)")
        else:
            logger.warning("Gemini API service: FAILED (falling back to mock responses)")
    else:
        logger.warning("Gemini API service: NOT CONFIGURED (using mock responses)")
    
    # Log CORS configuration on startup
    allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
    if allowed_origins_env:
        origins_list = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
        logger.info(f"CORS - Effective allowed origins: {origins_list}")
    else:
        logger.warning("CORS - ALLOWED_ORIGINS not set, using default origins")
    
    yield
    logger.info("Shutting down AI Copilot Backend Service")

# Create FastAPI app with metadata for OpenAPI documentation
app = FastAPI(
    title="AI Copilot Backend API",
    description="Backend service for AI Copilot web application. Handles chat requests, manages conversations, and integrates with Google Gemini API.",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check and service status endpoints"
        },
        {
            "name": "chat",
            "description": "Chat and conversation management endpoints"
        }
    ]
)

# Configure CORS
# Read ALLOWED_ORIGINS from environment and parse it properly
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")

if allowed_origins_env:
    # Parse comma-separated origins and strip whitespace
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
    logger.info(f"CORS - Using ALLOWED_ORIGINS from environment: {len(allowed_origins)} origins configured")
else:
    # Default origins including localhost and preview URLs
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:4000",
        "https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3000",
        "https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:4000",
        "https://vscode-internal-21410-beta.beta01.cloud.kavia.ai:3000",
        "https://vscode-internal-21410-beta.beta01.cloud.kavia.ai:4000"
    ]
    logger.warning("CORS - ALLOWED_ORIGINS not set in environment, using default origins")

# Add CORS middleware with explicit configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # List of exact origins (not wildcard when credentials=True)
    allow_credentials=True,  # Allow cookies and authorization headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers including Content-Type, Authorization, etc.
)

logger.info(f"CORS middleware configured with {len(allowed_origins)} allowed origins")
for origin in allowed_origins:
    logger.info(f"  - {origin}")

# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["health"],
    summary="Health Check",
    description="Check if the service is running and healthy",
    response_description="Service health status"
)
def health_check():
    """
    Health check endpoint to verify the service is running.
    
    Returns:
        A dictionary with health status and service information
    """
    return {
        "status": "healthy",
        "service": "AI Copilot Backend",
        "version": "1.0.0",
        "gemini_configured": gemini_service.api_key is not None
    }

# PUBLIC_INTERFACE
@app.get(
    "/health",
    tags=["health"],
    summary="Detailed Health Check",
    description="Get detailed health information about the service and its dependencies",
    response_description="Detailed health status"
)
def detailed_health():
    """
    Detailed health check endpoint with service status information.
    
    Returns:
        A dictionary with detailed health status including API configuration and CORS settings
    """
    # Get current CORS origins for verification
    allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
    if allowed_origins_env:
        cors_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
    else:
        cors_origins = [
            "http://localhost:3000",
            "http://localhost:4000",
            "https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:3000",
            "https://vscode-internal-25292-beta.beta01.cloud.kavia.ai:4000",
            "https://vscode-internal-21410-beta.beta01.cloud.kavia.ai:3000",
            "https://vscode-internal-21410-beta.beta01.cloud.kavia.ai:4000"
        ]
    
    return {
        "status": "healthy",
        "service": "AI Copilot Backend",
        "version": "1.0.0",
        "dependencies": {
            "gemini_api": {
                "configured": gemini_service.api_key is not None,
                "available": gemini_service.model is not None
            },
            "storage": {
                "type": "in-memory",
                "note": "TODO: Replace with persistent database"
            }
        },
        "cors": {
            "allowed_origins": cors_origins,
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"]
        }
    }

# PUBLIC_INTERFACE
@app.post(
    "/chat",
    tags=["chat"],
    summary="Send Chat Message",
    description="Send a message to the AI assistant and receive a response. Optionally continue an existing conversation by providing conversation_id.",
    response_model=ChatResponse,
    responses={
        200: {
            "description": "Successful response from AI assistant",
            "content": {
                "application/json": {
                    "example": {
                        "response": "Hello! How can I help you today?",
                        "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                        "timestamp": "2024-01-15T10:30:00Z"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error"
        }
    }
)
async def chat(request: ChatRequest):
    """
    Process a chat message and return an AI-generated response.
    
    This endpoint accepts a user message and optionally a conversation ID.
    If no conversation ID is provided, a new conversation is created.
    The message is sent to the Gemini API, and the response is stored
    along with the user's message in the conversation history.
    
    Args:
        request: ChatRequest containing the message and optional conversation_id
        
    Returns:
        ChatResponse with the AI's response, conversation_id, and timestamp
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        # Get or create conversation ID
        conversation_id = request.conversation_id
        if not conversation_id or not storage_service.conversation_exists(conversation_id):
            conversation_id = storage_service.create_conversation_id()
            logger.info(f"Created new conversation: {conversation_id}")
        else:
            logger.info(f"Continuing conversation: {conversation_id}")
        
        # Store user message
        storage_service.add_message(conversation_id, "user", request.message)
        
        # Get conversation history for context
        conversation_history = storage_service.get_conversation(conversation_id)
        
        # Generate AI response
        ai_response = await gemini_service.generate_response(
            request.message,
            conversation_history
        )
        
        # Store assistant response
        storage_service.add_message(conversation_id, "assistant", ai_response)
        
        logger.info(f"Generated response for conversation {conversation_id}")
        
        return ChatResponse(
            response=ai_response,
            conversation_id=conversation_id
        )
    
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat request: {str(e)}"
        )

# PUBLIC_INTERFACE
@app.get(
    "/history",
    tags=["chat"],
    summary="Get Conversation History",
    description="Retrieve the complete message history for a specific conversation ID",
    response_model=ConversationHistory,
    responses={
        200: {
            "description": "Conversation history retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                        "messages": [
                            {
                                "role": "user",
                                "content": "Hello!",
                                "timestamp": "2024-01-15T10:30:00Z"
                            },
                            {
                                "role": "assistant",
                                "content": "Hello! How can I help you today?",
                                "timestamp": "2024-01-15T10:30:01Z"
                            }
                        ]
                    }
                }
            }
        },
        404: {
            "description": "Conversation not found"
        }
    }
)
async def get_history(conversation_id: str):
    """
    Retrieve the complete conversation history for a given conversation ID.
    
    This endpoint returns all messages (both user and assistant) in chronological
    order for the specified conversation.
    
    Args:
        conversation_id: The UUID of the conversation to retrieve
        
    Returns:
        ConversationHistory containing the conversation_id and list of messages
        
    Raises:
        HTTPException: If the conversation_id doesn't exist (404)
    """
    try:
        if not storage_service.conversation_exists(conversation_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {conversation_id} not found"
            )
        
        messages = storage_service.get_conversation(conversation_id)
        
        # Convert to Message model format
        formatted_messages = [
            Message(
                role=msg["role"],
                content=msg["content"],
                timestamp=msg["timestamp"]
            )
            for msg in messages
        ]
        
        logger.info(f"Retrieved history for conversation {conversation_id}")
        
        return ConversationHistory(
            conversation_id=conversation_id,
            messages=formatted_messages
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving conversation history: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve conversation history: {str(e)}"
        )

# PUBLIC_INTERFACE
@app.get(
    "/conversations",
    tags=["chat"],
    summary="List All Conversations",
    description="Get a list of all conversation IDs in the system",
    response_description="List of conversation IDs"
)
async def list_conversations():
    """
    Get a list of all conversation IDs currently stored in the system.
    
    This is useful for the frontend to display a list of past conversations
    in the sidebar.
    
    Returns:
        A dictionary with a list of conversation IDs
    """
    try:
        conversation_ids = storage_service.get_all_conversation_ids()
        return {
            "conversations": conversation_ids,
            "count": len(conversation_ids)
        }
    except Exception as e:
        logger.error(f"Error listing conversations: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list conversations: {str(e)}"
        )

# PUBLIC_INTERFACE
@app.options("/conversations")
async def options_conversations():
    """
    Explicit OPTIONS handler for /conversations endpoint.
    Handles CORS preflight requests.
    """
    return {"status": "ok"}

# PUBLIC_INTERFACE
@app.options("/chat")
async def options_chat():
    """
    Explicit OPTIONS handler for /chat endpoint.
    Handles CORS preflight requests.
    """
    return {"status": "ok"}

# PUBLIC_INTERFACE
@app.options("/history")
async def options_history():
    """
    Explicit OPTIONS handler for /history endpoint.
    Handles CORS preflight requests.
    """
    return {"status": "ok"}
