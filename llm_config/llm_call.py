import requests

# Global variable to hold the Ollama API URL
ollama_api_url = "http://localhost:11434/api/generate"  # Updated URL

# Initialize conversation history
conversation_history = []
max_turns = 5  # Maximum number of turns to keep in the conversation history

def generate_text(prompt: str, model: str = "mistral:instruct"):
    """Generate text using the Ollama model with context."""
    global conversation_history  # Declare conversation_history as global

    # Append the new prompt to the conversation history
    conversation_history.append(f"User: {prompt}")

    # Limit the conversation history to the last 'max_turns' exchanges
    if len(conversation_history) > max_turns * 2:  # Each turn has a user and AI response
        conversation_history = conversation_history[-(max_turns * 2):]

    # Create a full prompt from the conversation history
    full_prompt = "\n".join(conversation_history) + "\nAI:"

    payload = {
        "model": model,  # Include the model in the payload
        "prompt": full_prompt,  # Use the limited conversation history as the prompt
        "stream": False  # Set to True for streaming if needed
    }
    
    response = requests.post(ollama_api_url, json=payload)
    if response.status_code == 200:
        ai_response = response.json().get("response", "")
        # Append the AI's response to the conversation history
        conversation_history.append(f"AI: {ai_response}")
        return ai_response  # Return the AI's response
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def reset_conversation():
    """Reset the conversation history."""
    global conversation_history
    conversation_history = []