from typing import List, Dict
from anthropic import Anthropic
from config import Config
from metadata import FinancialTableMetadata, LearningAnalyticsMetadata
from fuzzywuzzy import fuzz
from utils.search import search_financial_terms_without_threshold
from .llm_call import get_test_llm

class QueryDecomposer:
    def __init__(self):
        # Initialize the LLM directly without loading environment variables
        self.llm = get_test_llm("sonnet")  # LLM is now initialized here
        self.matcher = None
        self.financial_terms = {}
        self.metadata = LearningAnalyticsMetadata()

    def _decompose_complex_query(self, query: str) -> List[str]:
        """Break down complex learning analytics queries"""
        prompt = f"""Break down this learning analytics query into specific, focused sub-queries.
        
        Examples:
        1. Input: "What is the overall performance of students in Python programming?"
           Output: [
               "What is the average quiz score for Python programming?",
               "What is the course completion rate for Python programming?"
           ]
        
        2. Input: "Compare student engagement across different data science courses"
           Output: [
               "What is the engagement level in Introduction to Data Science?",
               "What is the engagement level in Advanced Data Science?"
           ]
        
        Current Query: {query}
        
        Return sub-queries that help provide a comprehensive analysis."""
        
        try:
            response = self.llm.messages.create(
                model=Config.sonnet_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=1000
            )
            sub_queries = [q.strip() for q in response.content[0].text.split('\n') if q.strip()]
            return sub_queries if sub_queries else [query]
        except Exception as e:
            print(f"Query decomposition failed: {e}")
            return [query]

    def _select_relevant_table(self, query: str) -> str:
        """Select the most relevant table based on query content using LLM"""
        tables_info = []
        for table_name, table_def in self.metadata.tables.items():
            table_info = (
                f"Table: {table_name}\n"
                f"Description: {table_def.description}\n"
                f"Common Queries: {', '.join(table_def.common_queries)}\n"
                f"Columns: {', '.join(f'{col} ({info.description})' for col, info in table_def.columns.items())}\n"
            )
            tables_info.append(table_info)

        prompt = (
            f"Given the following query and available tables, select the most appropriate table name.\n"
            f"Only return the table name, nothing else.\n\n"
            f"Query: {query}\n\n"
            f"Available Tables:\n{''.join(tables_info)}\n\n"
            "Table name:"
        )

        try:
            response = self.llm.messages.create(
                model=Config.sonnet_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=1000
            )
            selected_table = response.content[0].text.strip()
            if selected_table in self.metadata.tables:
                return selected_table
            return list(self.metadata.tables.keys())[0]
        except Exception as e:
            print(f"Table selection failed: {e}")
            return list(self.metadata.tables.keys())[0]

    def _initialize_matcher(self, table_metadata):
        """Initialize the matcher with table metadata"""
        self.financial_terms = {}
        for column_name, column_info in table_metadata.columns.items():
            if column_info.distinct_values:
                self.financial_terms[column_name] = column_info.distinct_values

    def _extract_entities(self, query: str, table_info) -> List[Dict]:
        """Extract entities using LLM-based entity extraction and fuzzy matching"""
        matches = search_financial_terms_without_threshold(query, table_info, self.llm)
        
        return [
            {
                "search_term": match["search_term"],
                "column": match["column"],
                "matched_value": match["matched_value"],
                "score": match["score"],
            }
            for match in matches
        ]

    def decompose_query(self, query: str) -> List[Dict]:
        """Main method to process and decompose queries"""
        try:
            sub_queries = self._decompose_complex_query(query)
            results = []
            for sub_query in sub_queries:
                table_name = self._select_relevant_table(sub_query)
                table_info = self.metadata.get_table_info(table_name)
                self._initialize_matcher(table_info)
                extracted_entities = self._extract_entities(sub_query, table_info)
                results.append({
                    "type": "direct" if len(sub_queries) == 1 else "decomposed",
                    "original_query": query,
                    "sub_query": sub_query,
                    "table": table_name,
                    "extracted_entities": extracted_entities,
                    "explanation": f"Query processed using {table_name} table",
                })
            return results
        except Exception as e:
            print(f"Warning: Query decomposition failed: {e}")
            return [{
                "type": "direct",
                "original_query": query,
                "sub_query": query,
                "extracted_entities": [],
                "explanation": "Direct query (fallback)",
            }]

    def find_entities(self, query: str) -> Dict[str, List[Dict]]:
        """Public method to find entities in a query"""
        table_name = self._select_relevant_table(query)
        table_info = self.metadata.get_table_info(table_name)
        self._initialize_matcher(table_info)
        extracted_entities = self._extract_entities(query, table_info)
        for entity in extracted_entities:
            entity["table"] = table_name
        return {
            "extracted_entities": extracted_entities,
        }
