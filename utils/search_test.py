from search import search_term_in_column

def main():
    # Test parameters
    table_name = "institution"
    column_name = "name"
    term = 'Mclaughlin, Jackson and White'
    
    # Call the search function
    match = search_term_in_column(term, table_name, column_name)
    
    # Print results
    print(f"\nSearch Results:")
    print(f"  Search term: '{match['search_term']}'")
    print(f"  Matched value: '{match['matched_value']}'")
    print(f"  Match score: {match['score']}")

if __name__ == "__main__":
    main()