import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from typing import Dict
from llm_config.llm_call import generate_text
from schema.metadata import SchemaMetadata, TYPE_CHOICES, GENDER_CHOICES, MODULE_TYPE_CHOICES, INSTITUTION_TYPE_CHOICES

class SQLGenerator:
    def main_generator(self, user_query: str, llm_model: str = "mistral:instruct") -> Dict:
        """
        Generate a single SQL query based on user query and database schema.
        The query can be simple or complex depending on the user's needs.
        
        Args:
            user_query: Natural language query from user
            llm_model: The LLM model to use for generation (default: "mistral:instruct")
            
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
            # Add table name and columns
            column_names = [col.name for col in columns]
            formatted_metadata.append(f"{table_name} ({', '.join(column_names)})")
            
            # Add choices information for columns that have them
            for col in columns:
                if hasattr(col, 'choices') and col.choices:
                    try:
                        if isinstance(col.choices[0], tuple):
                            choices_str = ', '.join([f"{k} ({v})" for k, v in col.choices])
                        else:
                            choices_str = ', '.join(str(choice) for choice in col.choices)
                        formatted_metadata.append(f"  - {col.name}: [{choices_str}]")
                    except Exception as e:
                        print(f"Warning: Could not format choices for column {col.name}: {str(e)}")
                        continue
            
            # Add a blank line between tables for readability
            formatted_metadata.append("")
        
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
- Ensure the query is complete and executable
- When filtering on columns with choices, use the exact choice values provided in the metadata"""
        
        generated_sql = generate_text(initial_prompt, model=llm_model)

        # 3. Return results
        return {
            "user_query": user_query,
            "formatted_metadata": formatted_metadata,
            "generated_sql": generated_sql
        }