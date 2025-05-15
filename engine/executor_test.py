import unittest
from executor import SQLExecutor

class TestSQLExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = SQLExecutor()

    def test_safe_query_execution(self):
        # Test a safe SELECT query
        query = "SELECT * FROM users LIMIT 5"
        result = self.executor.main_executor(query)
        self.assertIsNotNone(result)
        self.assertIn('formatted_results', result)
        self.assertIn('error', result)
        self.assertFalse(result['error'])

    def test_blocked_operations(self):
        # Test blocked operations
        blocked_queries = [
            "DROP TABLE users",
            "DELETE FROM users",
            "UPDATE users SET name = 'test'",
            "INSERT INTO users VALUES (1, 'test')",
            "TRUNCATE TABLE users"
        ]
        
        for query in blocked_queries:
            result = self.executor.main_executor(query)
            self.assertTrue(result['error'])
            self.assertIn('Blocked operation', result['formatted_results'])

    def test_invalid_query(self):
        # Test invalid SQL syntax
        query = "SELECT * FROM nonexistent_table"
        result = self.executor.main_executor(query)
        self.assertTrue(result['error'])
        self.assertIn('Error executing query', result['formatted_results'])

    def test_query_formatting(self):
        # Test query result formatting
        query = "SELECT id, name FROM users LIMIT 2"
        result = self.executor.main_executor(query)
        self.assertFalse(result['error'])
        formatted = result['formatted_results']
        self.assertIsInstance(formatted, str)
        self.assertIn('id', formatted.lower())
        self.assertIn('name', formatted.lower())

if __name__ == '__main__':
    unittest.main() 