import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from llm_config.llm_call import generate_text  # Import the generate_text function
from schema.metadata import SchemaMetadata
from utils.search import search_terms

class QueryDecomposer:
    def __init__(self):
        self.metadata = SchemaMetadata()  # Load schema metadata

    def decompose_complex_query(self, query):
        """
        Break down complex queries into specific sub-queries.
        """
        prompt = (
            f"Given the following query: {query}\n"
            "Provide the relevant sub-queries based on the examples below:\n"
            "1) Find all institutions in California offering computer science degrees\n"
            "   returned: ['Find all institutions in California offering computer science degrees']\n"
            "2) Compare the number of students in California pursuing computer science and biotechnology degrees\n"
            "   returned: ['Find number of students in California pursuing computer science degrees', 'Find number of students in California pursuing biotechnology degrees']\n"
            "Please return the relevant sub-queries as a list."
        )
        response = generate_text(prompt)  # Use generate_text instead of self.llm(prompt)
        
        # Extract sub-queries from the LLM response
        sub_queries = self.extract_sub_queries(response)
        return sub_queries

    def extract_sub_queries(self, response):
        # Logic to extract sub-queries from the LLM response
        return response.split(",")  # Example: split by commas

    def select_relevant_table(self, query):
        """
        Select the most appropriate table for a given query.
        """
        prompt = (
            f"Select the most appropriate table for the query: {query}\n"
            "Available tables: " + ", ".join(self.metadata.tables.keys()) + "\n"
            "Please return only the name of the single most relevant table and nothing else."
        )
        response = generate_text(prompt)  # Use generate_text instead of self.llm(prompt)
        return response.strip()  # Return the selected table name

    def extract_entities(self, query):
        """
        Extract entities from the query.
        """
        prompt = (
            f"Extract entities from the following query: {query}\n"
            "Example: 'Find all institutions in California offering computer science degrees.'\n"
            "Expected entities: ['California', 'computer science']\n"
            "Please return a list of entities."
        )
        response = generate_text(prompt)  # Use generate_text instead of self.llm(prompt)
        return self.parse_entities(response)  # Placeholder for parsing logic

    def parse_entities(self, response):
        # Logic to parse entities from the LLM response
        return response.split(",")  # Example: split by commas

    def match_entities(self, entity, table_name):
        """
        Find and map the entity to the table_name.
        """
        # Ensure the table name is properly quoted to prevent SQL syntax errors
        table_name = f'"{table_name}"'  # Quote the table name
        match = search_terms(entity, table_name)
        return match if match else []  # Return empty list on error

    def main_decomposer(self, query):
        """
        Main function to process the entire decomposer pipeline.
        """
        # First, check if decomposition is needed
        sub_queries = self.decompose_complex_query(query)
        
        results = []
        if len(sub_queries) == 1 and sub_queries[0] == query:
            # No decomposition needed, return original query
            table_name = self.select_relevant_table(query)
            entities = self.extract_entities(query)
            matches = [self.match_entities(entity, table_name) for entity in entities]
            
            result = {
                "query_type": "direct",
                "sub_query": query,
                "table_selected": table_name,
                "entities": entities,
                "matching_results": matches
            }
            results.append(result)
        else:
            # Decomposition is needed
            for sub_query in sub_queries:
                table_name = self.select_relevant_table(sub_query)
                entities = self.extract_entities(sub_query)
                matches = []
                
                for entity in entities:
                    match = self.match_entities(entity, table_name)
                    matches.append(match)
                
                result = {
                    "query_type": "decomposed",
                    "sub_query": sub_query,
                    "table_selected": table_name,
                    "entities": entities,
                    "matching_results": matches
                }
                results.append(result)
        
        return results
