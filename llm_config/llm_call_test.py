from llm_call import generate_text, reset_conversation  # Import the functions

# Reset conversation if starting fresh
reset_conversation()

# Define a prompt to test
prompt1 = "Tell me a joke."
response1 = generate_text(prompt1, model="mistral")  # Generate response for the first prompt
print("Generated Response 1:")
print(response1)

# Follow-up prompt
prompt2 = "Explain the joke."
response2 = generate_text(prompt2, model="mistral")  # Generate response for the follow-up
print("Generated Response 2:")
print(response2)