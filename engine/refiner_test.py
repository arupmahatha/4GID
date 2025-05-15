from refiner import SQLRefiner

def main():
    """Test SQL refinement functionality"""
    refiner = SQLRefiner()
    
    # Test SQL query
    sql_query = """SELECT * FROM Learner WHERE name = 'John Handcock';"""
    
    # Test value mappings
    value_mappings = [
        {
            "original_value": "John Handcock",
            "matched_value": "John Hancock",
            "score": 96
        }
    ]
    
    llm_model = "mistralai/Mistral-7B-Instruct-v0.3"
    
    print(f"\nTesting SQL Refinement:")
    print(f"\nInput SQL: '{sql_query}'")
    print(f"\nUsing LLM model: {llm_model}")
    print("\nValue Mappings:")
    for mapping in value_mappings:
        print("---")
        print(f"Original: '{mapping['original_value']}'")
        print(f"Matched: '{mapping['matched_value']}'")
        print(f"Score: {mapping['score']}")
       
    
    try:
        # Refine SQL
        results = refiner.main_refiner(sql_query, value_mappings, llm_model=llm_model)
        print(f"\nRefined SQL: {results['refined_sql']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 