from typing import List, Dict
from metadata import SchemaMetadata
from fuzzywuzzy import fuzz
from utils.search import search_financial_terms_without_threshold

class QueryDecomposer:
    def __init__(self, llm):
        self.llm = llm
        self.matcher = None
        self.financial_terms = {}
        self.metadata = SchemaMetadata()

    def _decompose_complex_query(self, query: str) -> List[str]:
        """Break down complex queries into specific, focused sub-queries"""
        prompt = f"""Determine if the given query requires decomposition or if it is simple enough to be returned as is. If the query is simple, return it directly. If decomposition is needed, break it down into specific, focused sub-queries that together help answer the main question.

        Examples:
        1. Input: "What is the performance of students in programming courses?"
           Output: "What is the performance of students in programming courses?"

        2. Input: "How do students from different institutions perform in programming courses, and what's their employment status after graduation?"
           Output: [
               "What is the performance of students in programming courses across different institutions?",
               "What is the employment status of students after graduation from these institutions?"
           ]

        Current Query: {query}

        If the query is simple enough, return it as is. If decomposition is needed, return a list of focused sub-queries that together help answer the main question. Each sub-query should be self-contained and focused on a specific aspect."""

        try:
            response = self.llm.invoke(prompt).content
            # Extract sub-queries from the response
            sub_queries = []
            for line in response.split('\n'):
                line = line.strip()
                if line and not line.startswith(('[', ']')) and '"' in line:
                    # Extract the query from between quotes
                    query_text = line.split('"')[1]
                    sub_queries.append(query_text)
            
            # If no sub-queries were extracted or something went wrong, return original query
            return sub_queries if sub_queries else [query]
            
        except Exception as e:
            print(f"Query decomposition failed: {e}")
            return [query]

    def _select_relevant_table(self, query: str) -> str:
        """Select the most relevant table based on query content using LLM"""
        # Prepare table information for the prompt
        tables_info = []
        for table_name in self.metadata.tables:
            relationships = self.metadata.get_relationships_for_table(table_name)
            
            table_info = (
                f"Table: {table_name}\n"
                f"Relationships: {', '.join(f'{rel.from_table}->{rel.to_table} ({rel.type})' for rel in relationships)}\n"
            )
            tables_info.append(table_info)

        prompt = f"""Given this query and the available tables, select the most appropriate table name.
        Consider the table's relationships. Return ONLY the exact table name, nothing else.

        Query: {query}

        Available Tables:
        {'\n'.join(tables_info)}

        Return only the table name that best matches the query requirements."""

        try:
            response = self.llm.invoke(prompt).content
            selected_table = response.strip()
            
            # Validate the selected table exists
            if selected_table in self.metadata.tables:
                return selected_table
                
            # Fallback to fuzzy matching if LLM returns invalid table
            best_match = None
            best_score = 0
            for table_name in self.metadata.tables:
                score = fuzz.ratio(selected_table.lower(), table_name.lower())
                if score > best_score:
                    best_score = score
                    best_match = table_name
            
            return best_match if best_match else list(self.metadata.tables.keys())[0]
            
        except Exception as e:
            print(f"Table selection failed: {e}")
            return list(self.metadata.tables.keys())[0]

    def _initialize_matcher(self, table_metadata):
        """Initialize the matcher with table metadata"""
        self.financial_terms = {}
        for column_name, column_info in table_metadata.columns.items():
            if column_info.distinct_values:
                self.financial_terms[column_name] = column_info.distinct_values

    def _extract_entities(self, query: str, table_info: Dict) -> List[Dict]:
        """Extract entities from the query and match them with table values"""
        try:
            # Use the search functionality to find matches
            matches = search_financial_terms_without_threshold(query, table_info, self.llm)
            
            # Format the matches
            formatted_matches = []
            for match in matches:
                formatted_match = {
                    "search_term": match["search_term"],
                    "column": match["column"],
                    "matched_value": match["matched_value"],
                    "score": match["score"]
                }
                formatted_matches.append(formatted_match)
            
            return formatted_matches
            
        except Exception as e:
            print(f"Entity extraction failed: {e}")
            return []

    def decompose_query(self, query: str) -> List[Dict]:
        """Main method to process and decompose queries"""
        try:
            # Step 1: Decompose complex query into sub-queries
            sub_queries = self._decompose_complex_query(query)
            
            results = []
            for idx, sub_query in enumerate(sub_queries, 1):
                try:
                    # Step 2: Select relevant table for each sub-query
                    table_name = self._select_relevant_table(sub_query)
                    
                    # Step 3: Get table info and extract entities
                    table_info = self.metadata.get_table_info(table_name)
                    extracted_entities = self._extract_entities(sub_query, table_info)
                    
                    # Create result for this sub-query
                    result = {
                        "sub_query_number": idx,
                        "original_query": query,
                        "sub_query": sub_query,
                        "table": table_name,
                        "table_info": table_info,
                        "extracted_entities": extracted_entities,
                        "type": "direct" if len(sub_queries) == 1 else "decomposed",
                        "explanation": f"Query processed using {table_name} table"
                    }
                    results.append(result)
                    
                except Exception as e:
                    # Handle individual sub-query failures
                    results.append({
                        "sub_query_number": idx,
                        "original_query": query,
                        "sub_query": sub_query,
                        "error": str(e),
                        "type": "failed"
                    })
            
            return results
            
        except Exception as e:
            print(f"Query decomposition failed: {e}")
            return [{
                "sub_query_number": 1,
                "original_query": query,
                "sub_query": query,
                "error": str(e),
                "type": "failed"
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
