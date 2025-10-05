from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., description="The user's message to send to the AI")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID to continue an existing conversation")

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="The AI assistant's response")
    conversation_id: str = Field(..., description="The conversation ID for this chat session")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the response")

class Message(BaseModel):
    """Model for a single message in conversation history"""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="When the message was sent")

class ConversationHistory(BaseModel):
    """Response model for conversation history endpoint"""
    conversation_id: str = Field(..., description="The conversation ID")
    messages: List[Message] = Field(default_factory=list, description="List of messages in the conversation")
