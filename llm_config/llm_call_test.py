from llm_call import generate_text, reset_conversation  # Import the functions

# Start with a fresh conversation
reset_conversation()

# First prompt
prompt1 = "Who are you?"
response1 = generate_text(prompt1, model="mistralai/Mistral-7B-Instruct-v0.3")
print("Generated Response 1:")
print(response1)

# Follow-up prompt without needing to include previous context (handled by conversation history)
prompt2 = "Tell me a joke."
response2 = generate_text(prompt2, model="mistralai/Mistral-7B-Instruct-v0.3")
print("\nGenerated Response 2:")
print(response2)