import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from llm_config.llm_call import generate_text

def get_file_content(file_path):
    """Read the content of a file."""
    with open(file_path, 'r') as f:
        return f.read()

def generate_metadata_updates():
    """Generate metadata.py updates using LLM."""
    # Get paths
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.py')
    metadata_path = os.path.join(os.path.dirname(__file__), 'metadata.py')
    
    # Read both files
    schema_content = get_file_content(schema_path)
    metadata_content = get_file_content(metadata_path)
    
    prompt = f"""Given this Django models schema:
{schema_content}

And this current metadata.py:
{metadata_content}

Identify and list only the changes or updates required in metadata.py to make it fully consistent with the schema.py.
Include additions, deletions, and modifications — covering all models, fields, choices, and relationships.
Do not return the entire updated file, just the specific diffs or instructions."""

    # Get the generated code from LLM
    generated_code = generate_text(prompt, model="deepseek-chat")
    
    print("\nSuggested updates for metadata.py:\n")
    print(generated_code)

if __name__ == "__main__":
    generate_metadata_updates()