import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from typing import Dict
from utils.schema_embeddings import SchemaEmbedder
from llm_call import generate_text
from schema.metadata import SchemaMetadata, TYPE_CHOICES, GENDER_CHOICES, MODULE_TYPE_CHOICES, INSTITUTION_TYPE_CHOICES

class SQLGenerator:
    def __init__(self):
        self.schema_embedder = SchemaEmbedder()

    def main_generator(self, user_query: str, llm_model: str = "mistral:instruct") -> Dict:
        """
        Generate a single SQL query using LLM based on user query and schema.
        The query can be simple or complex depending on the user's needs.
        
        Args:
            user_query: Natural language query from user
            llm_model: The LLM model to use for generation
            
        Returns:
            Dictionary containing metadata and the generated SQL query
        """
        # Get relevant schema information for the query
        formatted_metadata = self.schema_embedder.get_formatted_schema(user_query)

        # Create initial prompt
        prompt = f"""Given these tables and columns:
        {formatted_metadata}
        
        Generate a single SQL query for this request:
        {user_query}
        
        Requirements:
        - Return ONLY the raw SQL query text, no markdown formatting
        - Do not include ```sql or ``` markers
        - No explanations or additional text
        - The query can be simple or complex depending on what's needed
        - Use appropriate JOINs, subqueries, or aggregations if required
        - Ensure the query is complete and executable
        - When filtering on columns with choices, use the exact choice values provided in the metadata"""

        # Get SQL from LLM
        generated_sql = generate_text(prompt, model=llm_model)

        return {
            "user_query": user_query,
            "formatted_metadata": formatted_metadata,
            "generated_sql": generated_sql
        }