import unittest
from value_matcher import ValueMatcher

class TestValueMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = ValueMatcher()

    def test_exact_match(self):
        # Test exact value matching
        result = self.matcher.main_value_matcher(
            input_value="Active",
            table_name="users",
            column_name="status"
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertIn('value', result[0])
        self.assertIn('score', result[0])
        self.assertEqual(result[0]['score'], 100)

    def test_fuzzy_match(self):
        # Test fuzzy matching with similar values
        result = self.matcher.main_value_matcher(
            input_value="actv",
            table_name="users",
            column_name="status"
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        if len(result) > 0:
            self.assertGreaterEqual(result[0]['score'], 80)

    def test_no_matches(self):
        # Test when no matches are found
        result = self.matcher.main_value_matcher(
            input_value="nonexistent_value",
            table_name="users",
            column_name="status"
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_invalid_table(self):
        # Test with invalid table name
        result = self.matcher.main_value_matcher(
            input_value="test",
            table_name="nonexistent_table",
            column_name="status"
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_match_ordering(self):
        # Test that matches are ordered by score
        result = self.matcher.main_value_matcher(
            input_value="act",
            table_name="users",
            column_name="status"
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        if len(result) > 1:
            self.assertGreaterEqual(result[0]['score'], result[1]['score'])

if __name__ == '__main__':
    unittest.main() 