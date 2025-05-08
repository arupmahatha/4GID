# SQL Generation and Analysis System

A sophisticated system that leverages multiple Large Language Models (LLMs) to generate, validate, and execute SQL queries from natural language input. The system uses a multi-model approach with DeepSeek, Mistral, and Gemini for robust query generation and validation.

## Features

- **Multi-Model SQL Generation**: Utilizes multiple LLMs (DeepSeek and Mistral) to generate SQL queries from natural language
- **Intelligent Validation**: Uses Gemini as a decision maker to choose the best generated SQL query
- **Entity Extraction**: Extracts and analyzes entities from generated SQL queries
- **Value Matching**: Implements fuzzy matching for SQL values
- **Query Refinement**: Refines and optimizes generated SQL queries
- **Result Analysis**: Executes queries and provides detailed analysis of results

## Our Approach

### Multi-Model Architecture
Our system employs a unique multi-model architecture that combines the strengths of different LLMs:
- **DeepSeek**: Primary model for SQL generation with strong understanding of database schemas
- **Mistral**: Secondary model providing alternative SQL generation approaches
- **Gemini**: Acts as an intelligent validator to select the most accurate query

### Workflow Process
1. **Natural Language Processing**
   - Input query analysis
   - Entity recognition
   - Intent classification

2. **SQL Generation**
   - Parallel generation using multiple LLMs
   - Schema-aware query construction
   - Syntax validation

3. **Query Validation**
   - Cross-model comparison
   - Semantic analysis
   - Performance optimization

4. **Execution and Analysis**
   - Safe query execution
   - Result validation
   - Performance metrics collection

## Current Developments

### Active Research Areas
1. **Enhanced Entity Recognition**
   - Improving accuracy of entity extraction from natural language
   - Better handling of complex relationships between entities
   - Integration with domain-specific knowledge bases

2. **Query Optimization**
   - Development of more efficient SQL generation algorithms
   - Implementation of query performance prediction
   - Automated query optimization techniques

3. **Multi-Model Collaboration**
   - Advanced model selection strategies
   - Improved consensus mechanisms
   - Dynamic model weighting based on query type

### Recent Improvements
- Implemented fuzzy matching for better value recognition
- Enhanced error handling and recovery mechanisms
- Added support for complex nested queries
- Improved handling of temporal queries
- Integration of performance monitoring tools

### Upcoming Features
1. **Advanced Analytics**
   - Query pattern analysis
   - Usage statistics and insights
   - Performance optimization recommendations

2. **Extended Language Support**
   - Support for more natural language variations
   - Better handling of domain-specific terminology
   - Multi-language query support

3. **Enhanced Security**
   - Query sanitization improvements
   - Access control integration
   - Audit logging capabilities

## Project Structure

```
.
├── engine/                 # Core SQL generation and processing engine
├── llm_config/            # LLM configuration and API settings
├── schema/                # Database schema definitions
├── synthetic_data/        # Synthetic data for testing
├── test_cases_documentations/  # Test case documentation
├── utils/                 # Utility functions and helpers
├── report_documentations/ # Documentation for reports
├── workflow_test.ipynb    # Jupyter notebook demonstrating the workflow
└── requirements.txt       # Project dependencies
```

## Database Schema

The system works with a comprehensive database schema that includes:

- **Institution**: Educational institutions with various types (Public University, Private University, etc.)
- **Learner**: Student information including personal and educational details
- **Course**: Course information and structure
- **Program**: Academic programs and their requirements
- **Department**: Academic and non-academic departments
- **Knowledge Partner**: External knowledge partners
- **And more...**

## Prerequisites

- Python 3.8 or higher
- Access to LLM APIs (DeepSeek, Mistral, Gemini)
- SQLite database (or compatible database system)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- requests>=2.31.0
- python-dotenv>=1.0.0
- fuzzywuzzy>=0.18.0
- python-Levenshtein>=0.21.0
- sqlalchemy>=2.0.0
- pandas>=2.0.0
- numpy>=1.24.0
- faker>=20.0.0

## Usage

1. Set up your environment variables for LLM API access
2. Run the workflow test notebook:
```bash
jupyter notebook workflow_test.ipynb
```

The notebook demonstrates the complete workflow:
1. SQL generation using multiple LLMs
2. Entity extraction from SQL
3. Value matching in SQL
4. SQL refinement
5. Query execution
6. Result analysis

## Example Queries

The system can handle various types of queries, such as:
- Finding specific learners by name or email
- Analyzing student distributions by gender and age
- Querying institution-specific information
- Tracking course completion status
- Analyzing enrollment patterns