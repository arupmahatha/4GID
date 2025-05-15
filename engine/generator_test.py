import unittest
from generator import SQLGenerator

class TestSQLGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = SQLGenerator()

    def test_simple_query_generation(self):
        # Test simple query generation
        query = "Show me all users"
        result = self.generator.main_generator(query)
        
        self.assertIsNotNone(result)
        self.assertIn('user_query', result)
        self.assertIn('formatted_metadata', result)
        self.assertIn('generated_sql', result)
        self.assertEqual(result['user_query'], query)
        self.assertIsInstance(result['generated_sql'], str)
        self.assertTrue(result['generated_sql'].strip().upper().startswith('SELECT'))

    def test_complex_query_generation(self):
        # Test complex query with joins and aggregations
        query = "What is the average age of users by department?"
        result = self.generator.main_generator(query)
        
        self.assertIsNotNone(result)
        self.assertIn('generated_sql', result)
        sql = result['generated_sql'].upper()
        self.assertTrue('SELECT' in sql)
        self.assertTrue('FROM' in sql)
        self.assertTrue('GROUP BY' in sql)
        self.assertTrue('AVG' in sql)

    def test_query_with_choices(self):
        # Test query generation with column choices
        query = "Show me all active users"
        result = self.generator.main_generator(query)
        
        self.assertIsNotNone(result)
        self.assertIn('generated_sql', result)
        sql = result['generated_sql'].upper()
        self.assertTrue('SELECT' in sql)
        self.assertTrue('FROM' in sql)
        self.assertTrue('WHERE' in sql)
        self.assertTrue('STATUS' in sql or 'ACTIVE' in sql)

    def test_metadata_formatting(self):
        # Test schema metadata formatting
        query = "Show me all users"
        result = self.generator.main_generator(query)
        
        self.assertIsNotNone(result['formatted_metadata'])
        metadata = result['formatted_metadata']
        self.assertIsInstance(metadata, str)
        self.assertTrue(len(metadata) > 0)
        self.assertTrue('TABLE' in metadata.upper() or 'COLUMN' in metadata.upper())

if __name__ == '__main__':
    unittest.main() 