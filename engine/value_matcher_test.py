import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from engine.value_matcher import ValueMatcher

def main():
    """Test ValueMatcher functionality"""
    matcher = ValueMatcher()
    
    # Test case with a single entity
    test_entity = {
        "table": "admin_users",
        "column": "firstname",
        "value": "Chathnya"
    }
    
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