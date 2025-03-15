import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from typing import Dict, List
from llm_config.llm_call import generate_text
from utils.search import search_term_in_column

class SQLRefiner:
    def main_refiner(self, sql_query: str) -> Dict:
        """
        Extract entities from SQL and refine with matched values.
        
        Args:
            sql_query: SQL query to analyze and refine
            
        Returns:
            Dictionary containing:
                - original_sql: Input SQL query
                - extracted_entities: List of table, column, value mappings
                - value_mappings: List of matched values with scores
                - refined_sql: Refined or original SQL query
        """
        # 1. Extract entities
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
- ANY other output format is considered an error.

Query: {sql_query}"""

        entity_text = generate_text(extraction_prompt)
        print("text:\n")
        print(entity_text)
        # 2. Parse extracted entities and validate
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
            
        # If no valid entities after filtering
        if not extracted_entities:
            return {
                "original_sql": sql_query,
                "extracted_entities": [],
                "value_mappings": [],
                "refined_sql": sql_query
            }

        # 3. Search for matching values
        value_mappings = []
        for entity in extracted_entities:
            match = search_term_in_column(
                term=entity['value'],
                table_name=entity['table'],
                column_name=entity['column']
            )
            if match and match.get('score', 0) > 45:  # Only accept matches with score > 45
                value_mappings.append({
                    "original_value": entity['value'],
                    "matched_value": match['matched_value'],
                    "score": match['score']
                })

        # 4. Refine SQL if needed
        refined_sql = sql_query
        if value_mappings:
            refinement_prompt = f"""Return ONLY the modified SQL query with these replacements:
{chr(10).join(f"{m['original_value']} -> {m['matched_value']}" for m in value_mappings)}
Query: {sql_query}"""
            
            refined_sql = generate_text(refinement_prompt)

        # 5. Return results
        return {
            "original_sql": sql_query,
            "extracted_entities": extracted_entities,
            "value_mappings": value_mappings,
            "refined_sql": refined_sql
        } 