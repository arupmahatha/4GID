from entity_extractor import EntityExtractor

def main():
    """Test EntityExtractor functionality"""
    extractor = EntityExtractor()
    
    # Test query
    test_query = """SELECT l.name, l.email 
    FROM Learner l 
    WHERE l.name = 'David Gardner' 
    OR l.email = 'allisonthomson@example.com';"""
    
    llm_model = "mistral:instruct"  # Default model

    print("\nTesting Entity Extractor:")
    print(f"\nTest Query: {test_query}")
    print(f"\nUsing LLM model: {llm_model}")
    
    try:
        # Extract entities
        entities = extractor.main_entity_extractor(test_query, llm_model=llm_model)
        
        print("\nExtracted Entities:")
        if entities:
            for entity in entities:
                print("---")
                print(f"Table: {entity['table']}")
                print(f"Column: {entity['column']}")
                print(f"Value: {entity['value']}")
        else:
            print("No entities were extracted")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 