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
        extraction_prompt = f"""Extract table names, column names, and comparison values.
Return ONLY lines in format: table_name|column_name|comparison_value
Query: {sql_query}"""

        entity_text = generate_text(extraction_prompt)
        
        # 2. Parse extracted entities
        extracted_entities = []
        for line in entity_text.strip().split('\n'):
            if '|' in line:
                table, column, value = line.strip().split('|')
                extracted_entities.append({
                    "table": table.strip(),
                    "column": column.strip(),
                    "value": value.strip()
                })

        # 3. Search for matching values
        value_mappings = []
        for entity in extracted_entities:
            if entity['value'].lower() not in ['null', 'true', 'false'] and not entity['value'].replace('.','').isdigit():
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