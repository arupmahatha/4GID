I'll provide a comprehensive documentation for the SkillAggregator project, breaking it down into several key sections:

# SkillAggregator: E-Education Query Processing System

## 1. Project Overview
The SkillAggregator is an advanced AI-powered e-education query processing system designed to transform natural language queries into structured SQL queries, execute them, and provide intelligent analysis of the results.

## 2. System Architecture

### 2.1 Core Components
The system is composed of five primary components:

1. **QueryDecomposer** (`engine/decomposer.py`)
   - Breaks down complex queries into manageable sub-queries
   - Identifies relevant tables and extracts entities
   - Uses LLM (Claude Haiku/Sonnet) for intelligent query understanding

2. **SQLGenerator** (`engine/generator.py`)
   - Converts natural language sub-queries into valid SQL
   - Uses table metadata and extracted entities to construct precise queries
   - Ensures query safety and relevance

3. **SQLExecutor** (`engine/executor.py`)
   - Validates and executes SQL queries
   - Implements robust security checks
   - Prevents dangerous SQL operations
   - Converts query results into structured dictionary format

4. **SQLAnalyzer** (`engine/analyzer.py`)
   - Analyzes query results using LLM
   - Generates insights, trends, and educational implications
   - Provides structured JSON analysis

5. **QueryOrchestrator** (`engine/orchestrator.py`)
   - Coordinates the entire query processing workflow
   - Uses LangGraph for managing complex query processing steps
   - Handles error management and state tracking

### 2.2 Workflow Stages
The query processing follows these stages:
1. Query Decomposition
2. Table and Entity Selection
3. SQL Generation
4. Query Execution
5. Results Analysis

## 3. Key Technologies

### 3.1 Language Models
- **Claude Haiku**: Used for query decomposition and analysis
- **Claude Sonnet**: Used for SQL generation
- Provided by Anthropic's API

### 3.2 Libraries and Frameworks
- **Streamlit**: Web interface
- **LangChain**: LLM interaction
- **LangGraph**: Workflow orchestration
- **SQLite**: Database backend
- **FuzzyWuzzy**: Entity matching

## 4. Detailed Component Breakdown

### 4.1 QueryDecomposer
