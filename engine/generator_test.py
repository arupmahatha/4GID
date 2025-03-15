from generator import main_generator

def main():
    """Test SQL generation functionality"""
    
    # Test query
    query = "Evaluate the effectiveness of educational programs based on multiple metrics."

    print(f"\nQuery: '{query}'")
    
    try:
        # Generate SQL
        print("\nGenerating SQL...")
        results = main_generator(query)
        
        print("\nSchema Information:")
        print(results['formatted_metadata'])
        
        print("\nGenerated SQL:")
        print(results['generated_sql'])
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 