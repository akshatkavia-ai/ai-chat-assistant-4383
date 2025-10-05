import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-generativeai package not installed. Using mock responses.")

class GeminiService:
    """
    Service for interacting with Google Gemini API.
    Falls back to mock responses when API key is not configured or package is unavailable.
    """
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        
        if self.api_key and GENAI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini API initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini API: {e}")
                self.model = None
        else:
            if not self.api_key:
                logger.warning("GEMINI_API_KEY not found in environment. Using mock responses.")
            if not GENAI_AVAILABLE:
                logger.warning("google-generativeai package not available. Install with: pip install google-generativeai")
    
    # PUBLIC_INTERFACE
    async def generate_response(self, message: str, conversation_history: Optional[list] = None) -> str:
        """
        Generate a response from the Gemini API or return a mock response.
        
        Args:
            message: The user's message
            conversation_history: Optional list of previous messages for context
            
        Returns:
            The AI-generated response string
        """
        if not self.model:
            return self._mock_response(message)
        
        try:
            # Build context from conversation history if provided
            prompt = message
            if conversation_history:
                context = "\n".join([
                    f"{'User' if msg.get('role') == 'user' else 'Assistant'}: {msg.get('content', '')}"
                    for msg in conversation_history[-5:]  # Last 5 messages for context
                ])
                prompt = f"Previous conversation:\n{context}\n\nUser: {message}"
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return self._mock_response(message)
    
    def _mock_response(self, message: str) -> str:
        """
        Generate a mock response when Gemini API is unavailable.
        
        Args:
            message: The user's message
            
        Returns:
            A mock response string
        """
        return (
            f"[Mock Response - Gemini API not configured] "
            f"I received your message: '{message[:50]}{'...' if len(message) > 50 else ''}'. "
            f"To enable real AI responses, please set the GEMINI_API_KEY environment variable. "
            f"You can obtain an API key from https://makersuite.google.com/app/apikey"
        )
