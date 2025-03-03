from typing import Dict, List, Tuple, Annotated, TypedDict, Optional, Any
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, Graph
from langgraph.prebuilt.tool_executor import ToolExecutor
from langchain_core.tools import BaseTool, StructuredTool, tool
from langchain_core.exceptions import OutputParserException

from engine.decomposer import QueryDecomposer
from engine.generator import SQLGenerator
from engine.executor import SQLExecutor
from engine.analyzer import SQLAnalyzer

class GraphState(TypedDict):
    query: str
    decomposed_queries: List[Dict]
    generated_sql: List[Dict]
    query_results: List[Dict]
    final_analysis: Dict
    error: Optional[str]
    steps_output: List[Dict]  # Track detailed steps like test_workflow

class QueryOrchestrator:
    def __init__(self, llm: ChatAnthropic, db_connection):
        self.llm = llm
        self.decomposer = QueryDecomposer(self.llm)
        self.generator = SQLGenerator(self.llm)
        self.executor = SQLExecutor(db_connection)
        self.analyzer = SQLAnalyzer(self.llm)
        
        # Initialize graph
        self.workflow = self._create_workflow()

    def _handle_error(self, state: GraphState, step: str, error: Exception) -> GraphState:
        """Handle errors in a consistent way across all steps"""
        error_msg = f"Error in {step}: {str(error)}"
        state["error"] = error_msg
        state["steps_output"].append({
            "step": step,
            "error": error_msg,
            "status": "failed"
        })
        return state

    def _decompose_step(self, state: GraphState) -> GraphState:
        """Handle query decomposition step"""
        try:
            # First decompose into sub-queries
            sub_queries = self.decomposer._decompose_complex_query(state["query"])
            
            decomposition_details = []
            for idx, query in enumerate(sub_queries, 1):
                try:
                    # Get table for this sub-query
                    table = self.decomposer._select_relevant_table(query)
                    
                    # Get entities for this sub-query
                    table_info = self.decomposer.metadata.get_table_info(table)
                    self.decomposer._initialize_matcher(table_info)
                    entities = self.decomposer._extract_entities(query, table_info)
                    
                    detail = {
                        "sub_query_number": idx,
                        "query": query,
                        "table": table,
                        "entities": entities,
                        "table_info": table_info,
                        "type": "direct" if len(sub_queries) == 1 else "decomposed",
                        "explanation": f"Query processed using {table} table"
                    }
                    decomposition_details.append(detail)
                except Exception as e:
                    # Handle individual sub-query failures
                    detail = {
                        "sub_query_number": idx,
                        "query": query,
                        "error": str(e),
                        "type": "failed"
                    }
                    decomposition_details.append(detail)
            
            state["decomposed_queries"] = decomposition_details
            state["steps_output"].append({
                "step": "Query Understanding and Decomposition",
                "details": decomposition_details,
                "status": "completed"
            })
            return state
            
        except Exception as e:
            return self._handle_error(state, "Query Understanding and Decomposition", e)

    def _generate_step(self, state: GraphState) -> GraphState:
        """Handle SQL generation step"""
        try:
            generated_queries = []
            for query_info in state["decomposed_queries"]:
                if query_info.get("type") == "failed":
                    # Skip failed sub-queries
                    generated_queries.append(query_info)
                    continue
                    
                try:
                    # Generate SQL for this sub-query
                    query_data = {
                        'sub_query': query_info['query'],
                        'table': query_info['table'],
                        'entities': query_info['entities']
                    }
                    
                    sql = self.generator.generate_sql(query_data)
                    
                    # Validate SQL before proceeding
                    is_valid, error = self.executor.validate_query(sql)
                    if not is_valid:
                        raise ValueError(f"Invalid SQL generated: {error}")
                        
                    generated_queries.append({
                        **query_info,
                        "sql_query": sql
                    })
                except Exception as e:
                    # Handle individual SQL generation failures
                    generated_queries.append({
                        **query_info,
                        "error": str(e),
                        "type": "failed"
                    })
            
            state["generated_sql"] = generated_queries
            state["steps_output"].append({
                "step": "SQL Generation",
                "queries": generated_queries,
                "status": "completed"
            })
            return state
            
        except Exception as e:
            return self._handle_error(state, "SQL Generation", e)

    def _execute_step(self, state: GraphState) -> GraphState:
        """Handle SQL execution step"""
        try:
            execution_results = []
            for query_info in state["generated_sql"]:
                if query_info.get("type") == "failed":
                    # Skip failed queries
                    execution_results.append(query_info)
                    continue
                    
                try:
                    # Execute SQL and handle results
                    success, results, error = self.executor.execute_query(query_info["sql_query"])
                    if success:
                        execution_results.append({
                            **query_info,
                            "results": results
                        })
                    else:
                        raise ValueError(error)
                except Exception as e:
                    # Handle individual execution failures
                    execution_results.append({
                        **query_info,
                        "error": str(e),
                        "type": "failed",
                        "results": []
                    })
            
            state["query_results"] = execution_results
            state["steps_output"].append({
                "step": "Query Execution",
                "results": execution_results,
                "status": "completed"
            })
            return state
            
        except Exception as e:
            return self._handle_error(state, "Query Execution", e)

    def _analyze_step(self, state: GraphState) -> GraphState:
        """Handle results analysis step"""
        try:
            if state["query_results"]:
                try:
                    query_info = {"original_query": state["query"]}
                    analysis = self.analyzer.analyze_results(query_info, state["query_results"])
                    state["final_analysis"] = analysis
                    state["steps_output"].append({
                        "step": "Analysis",
                        "analysis": analysis,
                        "status": "completed"
                    })
                except Exception as e:
                    return self._handle_error(state, "Analysis", e)
            return state
            
        except Exception as e:
            return self._handle_error(state, "Analysis", e)

    def _create_workflow(self) -> Graph:
        """Create the workflow graph"""
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("decompose", self._decompose_step)
        workflow.add_node("generate", self._generate_step)
        workflow.add_node("execute", self._execute_step)
        workflow.add_node("analyze", self._analyze_step)
        
        # Add edges
        workflow.add_edge("decompose", "generate")
        workflow.add_edge("generate", "execute")
        workflow.add_edge("execute", "analyze")
        
        # Set entry and end points
        workflow.set_entry_point("decompose")
        workflow.set_finish_point("analyze")
        
        return workflow.compile()

    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a natural language query following test workflow structure"""
        try:
            # Initialize state
            state = {
                "query": query,
                "decomposed_queries": [],
                "generated_sql": [],
                "query_results": [],
                "final_analysis": {},
                "error": None,
                "steps_output": []
            }
            
            # Run the workflow
            final_state = self.workflow.invoke(state)
            
            return {
                "success": not bool(final_state["error"]),
                "error": final_state["error"],
                "steps": final_state["steps_output"],
                "analysis": final_state.get("final_analysis", {})
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "steps": state["steps_output"] if "state" in locals() else []
            } 