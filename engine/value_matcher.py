import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from typing import Dict, List
from utils.db_config import execute_query_pandas
from fuzzywuzzy import fuzz

class ValueMatcher:
    def main_value_matcher(self, entity: Dict) -> List[Dict]:
        """
        Find matching values in the database for a single extracted entity
        
        Args:
            entity: Dictionary containing table, column, value mapping
            
        Returns:
            List of dictionaries containing original value, matched value and match score
        """
        value_mappings = []
        min_match_score = 45

        try:
            # Get distinct values from the specified column
            query = f"""
            SELECT DISTINCT {entity['column']} as value
            FROM {entity['table']}
            WHERE {entity['column']} IS NOT NULL
            """
            
            results_df = execute_query_pandas(query)
            distinct_values = results_df['value'].tolist()

            best_match = None
            best_score = 0

            # Check each value for matches
            for value in distinct_values:
                # Convert value to string if needed
                if not isinstance(value, str):
                    value = str(value)

                # Calculate fuzzy match score
                score = fuzz.token_sort_ratio(entity['value'].lower(), value.lower())

                # Update if better match found
                if score > best_score:
                    best_score = score
                    best_match = {
                        'original_value': entity['value'],
                        'matched_value': value,
                        'score': score
                    }

            # Add match if score is above threshold
            if best_match and best_match['score'] > min_match_score:
                value_mappings.append(best_match)

        except Exception as e:
            print(f"Error matching values: {str(e)}")

        return value_mappings 