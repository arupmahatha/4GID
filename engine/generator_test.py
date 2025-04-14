from generator import SQLGenerator

def main():
    """Test SQL generation functionality"""
    generator = SQLGenerator()
    
    # Test query
    query = "What is the difference in count between male and female students."
    llm_model = "deepseek-chat"

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