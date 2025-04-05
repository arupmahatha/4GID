import os
import requests
import json

# Global variable to hold the Hugging Face API URL and key
huggingface_api_url = "https://api-inference.huggingface.co/models/"
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Global conversation history
conversation_history = []
max_turns = 5  # Maximum number of conversation turns to keep in history

def generate_text(prompt: str, model: str = "mistralai/Mistral-7B-Instruct-v0.3"):
    """Generate text using the Hugging Face model with conversation history."""
    global conversation_history
    
    # Add current prompt to history
    conversation_history.append({"role": "user", "content": prompt})
    
    # Prepare the context-aware prompt based on history
    if len(conversation_history) > 1:
        # Format the conversation history into a context string
        context_prompt = ""
        # Include up to max_turns previous exchanges
        start_idx = max(0, len(conversation_history) - (max_turns * 2))
        for i in range(start_idx, len(conversation_history)):
            entry = conversation_history[i]
            if entry["role"] == "user":
                context_prompt += f"User: {entry['content']}\n"
            else:
                context_prompt += f"Assistant: {entry['content']}\n"
        
        # Add the final instruction for the model
        final_prompt = context_prompt + "Assistant:"
    else:
        # For the first message, just use the prompt as is
        final_prompt = f"User: {prompt}\nAssistant:"
    
    # Set up the headers with your API key
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Format prompt based on model type
    if "mistral" in model.lower():
        formatted_prompt = f"<s>[INST] {final_prompt} [/INST]"
    else:
        formatted_prompt = final_prompt
    
    # Set up the payload
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.1,
            "top_p": 0.95,
            "do_sample": False,
            "return_full_text": False
        }
    }
    
    # Send the request to the specific model endpoint
    response = requests.post(f"{huggingface_api_url}{model}", headers=headers, json=payload)
    
    if response.status_code == 200:
        try:
            # Extract the generated text
            response_json = response.json()
            if isinstance(response_json, list) and len(response_json) > 0:
                generated_text = response_json[0].get("generated_text", "").strip()
                
                # Clean up any potential prefixes/formatting
                if "Assistant:" in generated_text:
                    generated_text = generated_text.split("Assistant:", 1)[1].strip()
                
                # Add the response to the conversation history
                conversation_history.append({"role": "assistant", "content": generated_text})
                
                # Trim history if needed
                if len(conversation_history) > max_turns * 2:
                    # Keep the most recent turns
                    conversation_history = conversation_history[-(max_turns * 2):]
                
                return generated_text
            return "Error: Unexpected API response format"
        except json.JSONDecodeError:
            return "Error: Invalid JSON response from API"
    else:
        error_msg = f"Error: {response.status_code} - {response.text}"
        print(error_msg)
        return error_msg

def reset_conversation():
    """Reset the conversation history."""
    global conversation_history
    conversation_history = []
    return True