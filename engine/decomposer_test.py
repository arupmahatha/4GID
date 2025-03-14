from decomposer import QueryDecomposer

def main():
    # Initialize the QueryDecomposer
    decomposer = QueryDecomposer()
    
    # Example user query
    user_query = "Find all institutions in California offering computer science degrees."
    
    # Process the user query
    results = decomposer.main_decomposer(user_query)
    
    # Print the results
    for result in results:
        print("Query Type:", result["query_type"])
        print("Sub Query:", result["sub_query"])
        print("Table Selected:", result["table_selected"])
        print("Entities:", result["entities"])
        print("Matching Results:", result["matching_results"])
        print("-" * 40)

if __name__ == "__main__":
    main()