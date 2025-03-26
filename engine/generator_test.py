from generator import SQLGenerator

def main():
    """Test SQL generation functionality"""
    generator = SQLGenerator()
    
    # Test query
    query = "Evaluate the effectiveness of educational programs based on multiple metrics."
    llm_model = "mistral:instruct"  # Default model

    print("\nTesting SQL Generator:")
    print(f"\nQuery: '{query}'")
    print(f"\nUsing LLM model: {llm_model}")
    
    try:
        # Generate SQL
        results = generator.main_generator(query, llm_model=llm_model)
        print("\nSchema Information:")
        print(results['formatted_metadata'])
        print("\nGenerated SQL:")
        print(results['generated_sql'])
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 