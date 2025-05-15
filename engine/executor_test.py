from executor import SQLExecutor

def main():
    """Test SQLExecutor functionality"""
    executor = SQLExecutor()

    test_query = """SELECT * FROM admin_users LIMIT 5"""

    print(f"Executing Query:\n{test_query}")
    
    success, results, formatted_results, error = executor.main_executor(test_query)
    
    if success:
        print(f"\nSuccess! Found {len(results)} rows")
        print("\nFormatted Results:")
        print(formatted_results)
        print("\nRaw Results:")
        print(results)
    else:
        print(f"\nFailed: {error}")

if __name__ == "__main__":
    main() 