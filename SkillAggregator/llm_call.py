import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT, APIError, APITimeoutError, APIConnectionError, RateLimitError
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from config import Config

# Load environment variables from .env file
load_dotenv()

def create_anthropic_client(api_key: Optional[str] = None) -> Anthropic:
    """Create an Anthropic client with proper error handling"""
    if api_key is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    
    return Anthropic(api_key=api_key)

def create_chat_anthropic(api_key: Optional[str] = None, model_name: Optional[str] = None, **kwargs) -> ChatAnthropic:
    """Create a ChatAnthropic instance with proper configuration"""
    if api_key is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
    if model_name is None:
        model_name = "claude-3-sonnet-20240229"
        
    return ChatAnthropic(
        anthropic_api_key=api_key,
        model=model_name,
        max_tokens=4096,
        temperature=0,
        **kwargs
    )

def handle_anthropic_error(error: Exception) -> Dict[str, Any]:
    """Handle various Anthropic API errors and return appropriate error information"""
    if isinstance(error, APITimeoutError):
        return {
            "error": "timeout",
            "message": "Request timed out. Please try again.",
            "status_code": 408
        }
    elif isinstance(error, RateLimitError):
        return {
            "error": "rate_limit",
            "message": "Rate limit exceeded. Please try again later.",
            "status_code": 429
        }
    elif isinstance(error, APIConnectionError):
        return {
            "error": "connection",
            "message": "Failed to connect to Anthropic API. Please check your internet connection.",
            "status_code": 503
        }
    elif isinstance(error, APIError):
        return {
            "error": "api_error",
            "message": str(error),
            "status_code": getattr(error, "status_code", 500)
        }
    else:
        return {
            "error": "unknown",
            "message": str(error),
            "status_code": 500
        }

def get_test_llm(model_type: str = "sonnet", api_key: Optional[str] = None, **kwargs):
    """Get test LLM client with appropriate model and error handling"""
    try:
        # Create base client
        client = create_anthropic_client(api_key)
        
        # Choose model based on type
        if model_type == "haiku":
            model = "claude-3-haiku-20240307"
        elif model_type == "opus":
            model = "claude-3-opus-20240229"
        else:  # default to sonnet
            model = "claude-3-sonnet-20240229"
            
        def wrapped_client(prompt: str):
            try:
                response = client.messages.create(
                    model=model,
                    max_tokens=4096,
                    temperature=0,
                    messages=[{"role": "user", "content": prompt}],
                    **kwargs
                )
                return response.content[0].text
            except Exception as e:
                error_info = handle_anthropic_error(e)
                raise RuntimeError(f"LLM call failed: {error_info['message']}")
        
        # Add invoke method to match object-style interface
        wrapped_client.api_key = api_key
        wrapped_client.invoke = lambda prompt: type('Response', (), {'content': wrapped_client(prompt)})()
        
        return wrapped_client
        
    except Exception as e:
        error_info = handle_anthropic_error(e)
        raise RuntimeError(f"Failed to initialize LLM client: {error_info['message']}") 