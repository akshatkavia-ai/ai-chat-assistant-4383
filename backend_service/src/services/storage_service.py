from typing import Dict, List, Optional
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

class StorageService:
    """
    In-memory storage for conversation history.
    
    TODO: Replace with persistent database storage (e.g., PostgreSQL, MongoDB)
    This is a temporary solution for development and testing.
    """
    
    def __init__(self):
        # Structure: {conversation_id: [{"role": "user/assistant", "content": "...", "timestamp": datetime}, ...]}
        self._conversations: Dict[str, List[Dict]] = {}
        logger.info("In-memory storage initialized (TODO: Replace with database)")
    
    # PUBLIC_INTERFACE
    def create_conversation_id(self) -> str:
        """
        Generate a new unique conversation ID.
        
        Returns:
            A new UUID string for the conversation
        """
        conversation_id = str(uuid.uuid4())
        self._conversations[conversation_id] = []
        logger.debug(f"Created new conversation: {conversation_id}")
        return conversation_id
    
    # PUBLIC_INTERFACE
    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: The conversation ID
            role: Either 'user' or 'assistant'
            content: The message content
        """
        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = []
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        self._conversations[conversation_id].append(message)
        logger.debug(f"Added {role} message to conversation {conversation_id}")
    
    # PUBLIC_INTERFACE
    def get_conversation(self, conversation_id: str) -> Optional[List[Dict]]:
        """
        Retrieve all messages from a conversation.
        
        Args:
            conversation_id: The conversation ID to retrieve
            
        Returns:
            List of message dictionaries or None if conversation doesn't exist
        """
        return self._conversations.get(conversation_id)
    
    # PUBLIC_INTERFACE
    def conversation_exists(self, conversation_id: str) -> bool:
        """
        Check if a conversation ID exists.
        
        Args:
            conversation_id: The conversation ID to check
            
        Returns:
            True if the conversation exists, False otherwise
        """
        return conversation_id in self._conversations
    
    # PUBLIC_INTERFACE
    def get_all_conversation_ids(self) -> List[str]:
        """
        Get all conversation IDs.
        
        Returns:
            List of all conversation IDs
        """
        return list(self._conversations.keys())
