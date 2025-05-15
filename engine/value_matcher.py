import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from typing import Dict, List
from utils.search import search_term_in_column

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
        match = search_term_in_column(
            term=entity['value'],
            table_name=entity['table'],
            column_name=entity['column']
        )
        if match and match.get('score', 0) > min_match_score:
            value_mappings.append({
                "original_value": entity['value'],
                "matched_value": match['matched_value'],
                "score": match['score']
            })
        return value_mappings 