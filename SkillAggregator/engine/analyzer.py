from typing import Dict, List
from .llm_call import get_test_llm

class SQLAnalyzer:
    def __init__(self):
        self.llm = get_test_llm("haiku")  # LLM is now initialized here

    def analyze_results(self, query_info: Dict, sub_query_results: List[Dict]) -> Dict:
        """Analyze SQL query results from multiple sub-queries and generate comprehensive insights"""
        try:
            # Format results for prompt
            formatted_results = self._format_sub_queries_for_prompt(sub_query_results)
            
            # Create prompt for analysis
            prompt = f"""
            Analyze the following SQL query results and provide insights.
            
            Original Query: {query_info['original_query']}
            
            Results:
            {formatted_results}
            
            Provide a detailed analysis in the following format:
            {{
                "summary": "<A clear summary of the query results>",
                "insights": ["<Key insight 1>", "<Key insight 2>", "<Key insight 3>"],
                "trends": ["<Observed trend 1>", "<Observed trend 2>"],
                "implications": ["<Business implication 1>", "<Business implication 2>"],
                "relationships": ["<Data relationship 1>", "<Data relationship 2>"]
            }}
            
            Ensure the response is in valid JSON format with the exact keys shown above.
            Each field except 'summary' should be an array of strings.
            """
            
            # Get analysis from LLM
            response_text = self.llm(prompt)

            # Clean and parse the response
            import json
            import re

            # Clean up the response text
            cleaned_text = response_text.strip()
            # Remove any markdown code block markers
            cleaned_text = re.sub(r'```json\s*|\s*```', '', cleaned_text)
            
            try:
                # First try to parse as JSON
                analysis = json.loads(cleaned_text)
                
                # Ensure proper structure
                if not isinstance(analysis.get('insights'), list):
                    analysis['insights'] = [analysis['insights']]
                if not isinstance(analysis.get('trends'), list):
                    analysis['trends'] = [analysis['trends']]
                if not isinstance(analysis.get('implications'), list):
                    analysis['implications'] = [analysis['implications']]
                if not isinstance(analysis.get('relationships'), list):
                    analysis['relationships'] = [analysis['relationships']]
                
            except json.JSONDecodeError:
                # Fallback analysis
                analysis = {
                    "summary": "Analysis results could not be properly formatted",
                    "insights": ["No specific insights could be extracted"],
                    "trends": ["No clear trends could be identified"],
                    "implications": ["Unable to determine business implications"],
                    "relationships": ["No clear relationships identified"]
                }
            
            return {
                "success": True,
                "analysis": analysis,
                "sub_query_count": len(sub_query_results),
                "total_result_count": sum(len(r.get('results', [])) for r in sub_query_results),
                "query_info": query_info
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query_info": query_info
            }

    def _format_sub_queries_for_prompt(self, formatted_results: List[Dict]) -> str:
        """Format multiple sub-query results for the analysis prompt"""
        output = []
        for idx, result in enumerate(formatted_results, 1):
            output.append(f"""
Sub-query {idx}:
Question: {result['sub_query']}
SQL Query: {result['sql_query']}
Results:
{result['results']}
""")
        return "\n".join(output)

    def _format_results_for_prompt(self, results: List[Dict]) -> str:
        """Format individual result set for the analysis prompt"""
        if not results:
            return "No results found"
            
        # Limit to first 10 rows for analysis
        sample_results = results[:10]
        formatted = []
        
        for row in sample_results:
            formatted.append(str(row))
            
        return "\n".join(formatted)

class LearningAnalyzer:
    def analyze_results(self, query_info: Dict, sub_query_results: List[Dict]) -> Dict:
        """Analyze learning analytics results"""
        prompt = f"""Analyze the following learning analytics results:

Original Query: {query_info['original_query']}

Provide insights in this format:
{{
    "summary": "<Overall learning performance summary>",
    "learning_insights": ["<Key learning trend 1>", "<Key learning trend 2>"],
    "skill_gaps": ["<Identified learning gaps>"],
    "recommendations": ["<Personalized learning recommendations>"],
    "engagement_analysis": ["<Student engagement observations>"]
}}
""" 