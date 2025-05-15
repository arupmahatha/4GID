from typing import Dict, List, Tuple
import re

import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.db_config import execute_query_with_columns

class SQLExecutor:
    # List of dangerous SQL operations to block
    BLOCKED_OPERATIONS = {'delete', 'drop', 'truncate', 'update', 'insert', 'replace', 'alter', 'create', 'rename', 'modify', 'grant', 'revoke'}
    
    # List of allowed query starting terms
    ALLOWED_STARTS = {'select', 'with'}

    def _is_safe_query(self, sql_query: str) -> Tuple[bool, str]:
        """
        Check if the query is safe to execute
        Returns:
            Tuple of (is_safe: bool, error_message: str)
        """
        # Convert to lowercase for checking
        query_lower = sql_query.lower().strip()
        
        # Check if query starts with allowed terms
        is_allowed_start = any(query_lower.startswith(term) for term in self.ALLOWED_STARTS)
        if not is_allowed_start:
            return False, f"Query must start with one of: {', '.join(self.ALLOWED_STARTS)}"

        # Check for blocked operations
        for operation in self.BLOCKED_OPERATIONS:
            # Use regex to find whole words only
            pattern = r'\b' + operation + r'\b'
            if re.search(pattern, query_lower):
                return False, f"Operation '{operation}' is not allowed"

        return True, ""

    def format_results_for_analysis(self, results: List[Dict]) -> str:
        """
        Format query results into clear, tabular text for LLM analysis
        Args:
            results: List of dictionaries containing query results
        Returns:
            Formatted string representation of results
        """
        if not results:
            return "No results found"

        # Get column names from first result
        columns = list(results[0].keys())
        
        # Calculate column widths
        col_widths = {col: len(col) for col in columns}
        for row in results:
            for col in columns:
                col_widths[col] = max(col_widths[col], len(str(row[col])))

        # Create header
        header = " | ".join(col.ljust(col_widths[col]) for col in columns)
        separator = "-" * len(header)

        # Format rows
        formatted_rows = []
        for row in results:
            formatted_row = " | ".join(str(row[col]).ljust(col_widths[col]) for col in columns)
            formatted_rows.append(formatted_row)

        # Combine all parts
        return "\n".join([header, separator] + formatted_rows)

    def main_executor(self, sql_query: str) -> Tuple[bool, List[Dict], str, str]:
        """
        Validate and execute SQL query safely
        Returns:
            Tuple containing:
            - success: bool
            - results: List of dictionaries (row results)
            - formatted_results: Formatted string representation of results
            - error: Error message if any
        """
        # First check if query is safe
        is_safe, error_msg = self._is_safe_query(sql_query)
        if not is_safe:
            return False, [], "", error_msg

        try:
            # Execute the query using the new db_config utility
            columns, rows = execute_query_with_columns(sql_query)
            results = [dict(zip(columns, row)) for row in rows]
            formatted_results = self.format_results_for_analysis(results)
            return True, results, formatted_results, ""
        except Exception as e:
            return False, [], "", str(e) 