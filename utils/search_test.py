import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.search import search_term_in_column

def main():
    # Test parameters
    table_name = "admin_users"
    column_name = "firstname"
    term = 'Chathnya'
    
    # Call the search function
    match = search_term_in_column(term, table_name, column_name)
    
    # Print results
    print(f"\nSearch Results:")
    print(f"  Search term: '{match['search_term']}'")
    print(f"  Matched value: '{match['matched_value']}'")
    print(f"  Match score: {match['score']}")

if __name__ == "__main__":
    main()