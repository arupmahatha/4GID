import os
from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer

def download_and_install_gpt_neo(model_name: str = "EleutherAI/gpt-neo-1.3B", save_directory: str = "./gpt_neo_model"):
    """Download and install the GPT-Neo model and tokenizer for later use."""
    os.makedirs(save_directory, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(save_directory)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.save_pretrained(save_directory)
    print(f"Model and tokenizer downloaded and saved to {save_directory}")

def initialize_llm(model_name: str = "EleutherAI/gpt-neo-1.3B"):
    """Initialize LLM client and return a callable function."""
    download_and_install_gpt_neo(model_name)  # Ensure the model is downloaded
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_text(prompt: str):
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=100)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generate_text

# Example usage
generate_text = initialize_llm() 