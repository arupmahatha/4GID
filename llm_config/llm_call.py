import os
import requests
import json

# Global variables for API configurations
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
huggingface_api_url = "https://api-inference.huggingface.co/models/"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Global conversation history
conversation_history = []
max_turns = 5  # Maximum number of conversation turns to keep in history

def generate_text(prompt: str, model: str = "mistralai/Mistral-7B-Instruct-v0.3"):
    """Generate text using either Hugging Face, DeepSeek, or Gemini model with conversation history."""
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
    
    # Check which model to use
    if "deepseek" in model.lower():
        return _call_deepseek_api(final_prompt, model)
    elif "gemini" in model.lower():
        return _call_gemini_api(final_prompt, model)
    else:
        return _call_huggingface_api(final_prompt, model)

def _call_huggingface_api(prompt: str, model: str):
    """Make API call to Hugging Face models."""
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Format prompt based on model type
    if "mistral" in model.lower():
        formatted_prompt = f"<s>[INST] {prompt} [/INST]"
    else:
        formatted_prompt = prompt
    
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
    
    response = requests.post(f"{huggingface_api_url}{model}", headers=headers, json=payload)
    
    if response.status_code == 200:
        try:
            response_json = response.json()
            if isinstance(response_json, list) and len(response_json) > 0:
                generated_text = response_json[0].get("generated_text", "").strip()
                if "Assistant:" in generated_text:
                    generated_text = generated_text.split("Assistant:", 1)[1].strip()
                _update_conversation_history(generated_text)
                return generated_text
            return "Error: Unexpected API response format"
        except json.JSONDecodeError:
            return "Error: Invalid JSON response from API"
    else:
        error_msg = f"Error: {response.status_code} - {response.text}"
        print(error_msg)
        return error_msg

def _call_deepseek_api(prompt: str, model: str):
    """Make API call to DeepSeek models."""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Format messages for DeepSeek API
    messages = []
    for entry in conversation_history:
        messages.append({
            "role": entry["role"],
            "content": entry["content"]
        })
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": 512
    }
    
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        try:
            response_json = response.json()
            generated_text = response_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            _update_conversation_history(generated_text)
            return generated_text
        except (json.JSONDecodeError, KeyError, IndexError):
            return "Error: Invalid API response format"
    else:
        error_msg = f"Error: {response.status_code} - {response.text}"
        print(error_msg)
        return error_msg

def _call_gemini_api(prompt: str, model: str):
    """Make API call to Gemini models using REST API."""
    headers = {
        "Content-Type": "application/json"
    }
    
    # Format the request payload
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "topP": 0.95,
            "maxOutputTokens": 512
        }
    }
    
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_json = response.json()
            generated_text = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
            _update_conversation_history(generated_text)
            return generated_text
        else:
            error_msg = f"Error: {response.status_code} - {response.text}"
            print(error_msg)
            return error_msg
            
    except Exception as e:
        error_msg = f"Error calling Gemini API: {str(e)}"
        print(error_msg)
        return error_msg

def _update_conversation_history(generated_text: str):
    """Update conversation history with the generated response."""
    global conversation_history
    conversation_history.append({"role": "assistant", "content": generated_text})
    
    # Trim history if needed
    if len(conversation_history) > max_turns * 2:
        conversation_history = conversation_history[-(max_turns * 2):]

def reset_conversation():
    """Reset the conversation history."""
    global conversation_history
    conversation_history = []
    return True