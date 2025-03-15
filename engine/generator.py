import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from typing import Dict
from llm_config.llm_call import generate_text
from schema.metadata import SchemaMetadata

def main_generator(user_query: str) -> Dict:
    """
    Generate a single SQL query based on user query and database schema.
    The query can be simple or complex depending on the user's needs.
    
    Args:
        user_query: Natural language query from user
        
    Returns:
        Dictionary containing:
            - user_query: Original user query
            - formatted_metadata: Formatted table and column information
            - generated_sql: Single SQL query (no additional text/explanations)
    """
    # Get metadata instance
    metadata = SchemaMetadata()

    # 1. Format table and column information
    formatted_metadata = []
    for table_name, columns in metadata.tables.items():
        column_names = [col.name for col in columns]
        formatted_metadata.append(f"{table_name} ({', '.join(column_names)})")
    formatted_metadata = "\n".join(formatted_metadata)

    # 2. Generate SQL
    initial_prompt = f"""Given these tables and columns:
{formatted_metadata}

Generate a single SQL query for this request:
{user_query}

Requirements:
- Return ONLY the raw SQL query text, no markdown formatting
- Do not include ```sql or ``` markers
- No explanations or additional text
- The query can be simple or complex depending on what's needed
- Use appropriate JOINs, subqueries, or aggregations if required
- Ensure the query is complete and executable"""
    
    generated_sql = generate_text(initial_prompt)

    # 3. Return results
    return {
        "user_query": user_query,
        "formatted_metadata": formatted_metadata,
        "generated_sql": generated_sql
    }