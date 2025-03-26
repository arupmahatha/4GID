from value_matcher import ValueMatcher

def main():
    """Test ValueMatcher functionality"""
    matcher = ValueMatcher()
    
    # Test case with a single entity
    test_entity = {
        "table": "Learner",
        "column": "name",
        "value": "David Gardner"
    }
    
    print(f"\nTesting Value Matcher:")
    print("\nInput Entity:")
    print(f"Table: {test_entity['table']}")
    print(f"Column: {test_entity['column']}")
    print(f"Value: {test_entity['value']}")
    
    try:
        # Find matches
        matches = matcher.main_value_matcher(test_entity)
        
        print("\nMatched Value:")
        if matches:
            for match in matches:
                print(f"Original: '{match['original_value']}'")
                print(f"Matched: '{match['matched_value']}'")
                print(f"Score: {match['score']}")
        else:
            print("No matches found")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 