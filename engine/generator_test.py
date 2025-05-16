from generator import SQLGenerator

def main():
    """Test SQL generation functionality"""
    generator = SQLGenerator()
    
    # Test query
    query = "Show the FPS Inspection Allocation Report from May 1, 2025 to May 14, 2025 for district 209, sub-division 07001, block 01116, panchayat 000377, assigned by dayakarB, and assigned to 40015297."
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