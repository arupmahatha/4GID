from refiner import SQLRefiner

def main():
    """Test SQL refinement functionality"""
    refiner = SQLRefiner()
    
    # Test SQL query
    sql_query = """
    SELECT * FROM Learner WHERE name = 'John Handcock';
    """
    print(f"\nInput SQL: '{sql_query}'")
    
    try:
        # Refine SQL
        print("\nRefining SQL...")
        results = refiner.main_refiner(sql_query)
        
        print("\nExtracted Entities:")
        for entity in results['extracted_entities']:
            print(f"Table: {entity['table']}")
            print(f"Column: {entity['column']}")
            print(f"Value: {entity['value']}")
            print("---")
        
        print("\nValue Mappings:")
        if results['value_mappings']:
            for mapping in results['value_mappings']:
                print(f"Original: '{mapping['original_value']}'")
                print(f"Matched: '{mapping['matched_value']}'")
                print(f"Score: {mapping['score']}")
                print("---")
        else:
            print("No value mappings needed")
        
        print("\nRefined SQL:")
        print(results['refined_sql'])
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 