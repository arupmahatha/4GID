from typing import Dict, List
from config import Config
from ...metadata import LearningAnalyticsMetadata
import os
from ..llm_config.llm_call import get_test_llm

class SQLGenerator:
    def __init__(self):
        # Initialize the LLM directly with GPT-Neo
        self.llm = get_test_llm("gpt-neo")  # Updated to use GPT-Neo
        self.metadata = LearningAnalyticsMetadata()

    def generate_sql(self, query_info: Dict) -> str:
        """Generate SQL for learning analytics queries"""
        prompt = f"""Generate a SQL query for learning analytics:

Query: {query_info['sub_query']}
Table: student_performance

Requirements:
1. Use only columns from student_performance
2. Focus on extracting meaningful learning insights
3. Use appropriate aggregation functions
4. Consider student progress and engagement metrics
"""

        sql_query = self.llm.messages.create(
            model=Config.sonnet_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=1000
        ).content[0].text.strip()
        
        # Basic validation
        if not sql_query.lower().startswith('select'):
            raise ValueError("Generated query must start with SELECT")
        
        return sql_query

    def _format_table_schema(self, table_info) -> str:
        """Format available columns for the prompt"""
        schema = []
        for col_name, col_info in table_info.columns.items():
            schema.append(f"- {col_name}: {col_info.description}")
        return "\n".join(schema)

    def _format_entity_matches(self, entity_matches: List[Dict], table_info) -> str:
        """Format entity matches using the extracted entities"""
        if not entity_matches:
            return "No specific entity matches found"
        
        matches = []
        for match in entity_matches:
            matches.append(
                f"- Found '{match['search_term']}' in column '{match['column']}' "
                f"matching value '{match['matched_value']}'"
            )
        
        return "\n".join(matches) 