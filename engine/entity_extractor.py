import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from typing import Dict, List
from llm_config.llm_call import generate_text

class EntityExtractor:
    def main_entity_extractor(self, sql_query: str, llm_model: str = "mistral:instruct") -> List[Dict]:
        """
        Extract entities from SQL query
        
        Args:
            sql_query: SQL query to analyze
            llm_model: The LLM model to use for extraction (default: "mistral:instruct")
            
        Returns:
            List of dictionaries containing table, column, value mappings
        """
        extraction_prompt = f"""You are an SQL entity extractor. Your ONLY task is to extract real-world entities.

Format: table_name|column_name|comparison_value

Step 1 - SQL Structure Analysis:
1. First identify the actual database tables (not views/CTEs):
   - CTEs (WITH clause) are temporary views, NEVER use them as table names
   - Subqueries are temporary views, NEVER use them as table names
   - Table aliases (e.g., 'p', 't1') are shortcuts, NEVER use them as table names

2. For each column, trace its true origin:
   - Follow the JOIN chain to find the source table
   - Resolve aliases to full table names (e.g., 'p.name' comes from 'Program.name')
   - Identify computed columns (they are not real data)

Step 2 - Entity Identification:
ONLY extract entities that meet ALL these criteria:
1. Table name must be:
   - An actual database table (not a CTE, view, or alias)
   - The original source table (not an intermediate join)

2. Column must be:
   - A real data column (not computed/derived)
   - From the source table (not aggregated or transformed)
   - Storing actual entity data (names, descriptions, IDs, etc.)

3. Comparison value must be:
   - An actual specific value being compared
   - Not NULL
   - Not a mathematical comparison (>, <, >=, <=)
   - Not a logical condition (AND, OR, NOT)
   - Not a pattern match (LIKE, IN)
   - Not a number or boolean

NEVER output any of these:
- NULL values in any field
- CTE names as table names (e.g., 'ProgramMetrics')
- Table aliases as table names (e.g., 'p' instead of 'Program')
- Computed/derived columns
- Aggregated fields (COUNT, SUM, AVG, etc.)
- Mathematical comparisons
- Columns without specific value comparisons

Example Valid Extractions:
Program|name|John Smith              # Real table, real column, specific value
Student|email|alice@example.com      # Real table, real column, specific value

Example Invalid Extractions (NEVER output these):
ProgramMetrics|count|5               # Uses CTE as table
p|name|NULL                          # Uses alias and NULL
Program|enrolled_learners|>0         # Mathematical comparison
Program|avg_completion_time|3.5      # Computed column

CRITICAL INSTRUCTIONS:
- If no valid entities are found, return ABSOLUTELY NOTHING. Not even empty lines or explanations.
- ONLY output the exact table_name|column_name|comparison_value format for valid entities.
- ANY other output format is considered an error."""
        
        # Get entity mapping from LLM
        entity_text = generate_text(f"{extraction_prompt}\n\nQuery: {sql_query}", model=llm_model)
        
        # Parse and validate extracted entities
        extracted_entities = []
        for line in entity_text.strip().split('\n'):
            if '|' not in line:
                continue
                
            table, column, value = line.strip().split('|')
            table = table.strip()
            column = column.strip()
            value = value.strip()
            
            # Skip invalid entries
            if (value.upper() == 'NULL' or                # No NULL values
                table.startswith('p.') or                 # No table aliases
                any(x in value for x in ['>', '<', '=', 'NULL']) or  # No comparisons
                value.replace('.','').isdigit()):         # No numbers
                continue
                
            extracted_entities.append({
                "table": table,
                "column": column,
                "value": value
            })
            
        return extracted_entities 