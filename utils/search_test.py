import unittest

# Now import the modules after adding to path
from search import search_terms

class TestSearch(unittest.TestCase):

    def test_search_terms(self):
        table_name = "Institution"  # Name of the table to search
        term = 'Mclaughlin, Jackson and White' # Define the test term
        
        # Call the search function
        match = search_terms(term, table_name)
        
        # Verify results
        self.assertIsNotNone(match)
        print(f"\nFound match in column '{match['column']}':")
        print(f"  Search term: '{match['search_term']}'")
        print(f"  Matched value: '{match['matched_value']}'")
        print(f"  Match score: {match['score']}")

if __name__ == "__main__":
    unittest.main()