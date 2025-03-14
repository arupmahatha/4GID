from typing import Dict
from fuzzywuzzy import fuzz
import sqlite3

def search_terms(term: str, table_name: str) -> Dict:
    """
    Find the best match for the term in the table.
    Returns the best match for the term.
    """
    # Connect to the database
    conn = sqlite3.connect('our_database.db')
    cursor = conn.cursor()

    # 1. Validate table_name exists and has columns
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    
    if not columns_info:
        raise ValueError(f"Table '{table_name}' not found in the database.")

    # Prepare column data
    columns = [{'name': col[1], 'distinct_values': []} for col in columns_info]

    # Fetch distinct values for each column
    for column in columns:
        cursor.execute(f"SELECT DISTINCT {column['name']} FROM {table_name}")
        column['distinct_values'] = [row[0] for row in cursor.fetchall()]

    best_match = None
    best_score = 0
    
    # Check each column
    for column in columns:
        # Only check columns with distinct values
        if column['distinct_values']:
            for value in column['distinct_values']:
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
                        'column': column['name'],
                        'score': score
                    }
    
    # 3. Return best match if found, else return empty dictionary
    return best_match if best_match else {}