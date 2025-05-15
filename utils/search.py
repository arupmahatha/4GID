from utils.db_config import execute_query_with_columns
from typing import Dict
from fuzzywuzzy import fuzz

def search_term_in_column(term: str, table_name: str, column_name: str) -> Dict:
    """
    Find the best match for the term in the specified column of the table.
    Args:
        term: The term to search for
        table_name: The name of the table to search in
        column_name: The name of the column to search in
    Returns:
        Dictionary containing the search term, matched value and score, or empty dict if no match found
    """
    # Validate table and column exist by attempting to query
    try:
        query = f"SELECT DISTINCT {column_name} FROM {table_name}"
        columns, rows = execute_query_with_columns(query)
        if not rows:
            return {}
        distinct_values = [row[0] for row in rows]
    except Exception as e:
        # Table or column does not exist, or query failed
        return {}

    best_match = None
    best_score = 0
    for value in distinct_values:
        if value is None:
            continue
        if not isinstance(value, str):
            value = str(value)
        score = fuzz.token_sort_ratio(term.lower(), value.lower())
        if score > best_score:
            best_score = score
            best_match = {
                'search_term': term,
                'matched_value': value,
                'score': score
            }
    return best_match if best_match else {}