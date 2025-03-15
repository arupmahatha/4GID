from typing import Dict
from fuzzywuzzy import fuzz
import sqlite3

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
    # Connect to the database
    conn = sqlite3.connect('/Users/arup/Documents/4GID/our_database.db')
    cursor = conn.cursor()

    try:
        # Validate table and column exist
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        if not columns:
            raise ValueError(f"Table '{table_name}' not found in the database.")
            
        if not any(col[1] == column_name for col in columns):
            raise ValueError(f"Column '{column_name}' not found in table '{table_name}'.")

        # Get distinct values from specified column
        cursor.execute(f"SELECT DISTINCT {column_name} FROM {table_name}")
        distinct_values = [row[0] for row in cursor.fetchall()]

        best_match = None
        best_score = 0
        
        # Check each value for matches
        for value in distinct_values:
            # Convert value to string if needed
            if not isinstance(value, str):
                value = str(value)
            
            # Calculate fuzzy match score
            score = fuzz.token_sort_ratio(term.lower(), value.lower())
            
            # Update if better match found
            if score > best_score:
                best_score = score
                best_match = {
                    'search_term': term,
                    'matched_value': value,
                    'score': score
                }
        
        return best_match if best_match else {}

    finally:
        conn.close()