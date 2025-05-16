# SQL Generation and Analysis System

A sophisticated system that leverages multiple Large Language Models (LLMs) to generate, refine, and analyze SQL queries from natural language input. The system uses an ensemble approach with DeepSeek, Mistral, and Gemini models to ensure high-quality SQL generation and validation.

## System Architecture

The system is built with a modular architecture consisting of several key components:

### 1. LLM Configuration (`llm_config/`)
- Manages interactions with multiple LLM providers (HuggingFace, DeepSeek, Gemini)
- Handles API calls, conversation history, and response formatting
- Supports multiple models with configurable parameters
- Maintains conversation context for improved response quality

### 2. Core Engine Components (`engine/`)

#### SQL Generator
- Converts natural language queries into SQL using LLMs
- Integrates with schema embedder for context-aware generation
- Supports complex queries with JOINs, subqueries, and aggregations
- Ensures SQL syntax correctness and completeness

#### Entity Extractor
- Analyzes generated SQL to identify real-world entities
- Extracts table, column, and value mappings
- Filters out computed columns, aliases, and invalid entities
- Maintains strict validation rules for entity extraction

#### Value Matcher
- Matches extracted entities against database values
- Validates entity existence and relationships
- Ensures data consistency and accuracy

#### SQL Refiner
- Refines generated SQL based on entity matching results
- Optimizes query structure and performance
- Ensures query correctness and efficiency

#### SQL Executor
- Executes refined SQL queries against the database
- Handles query execution and result retrieval
- Manages database connections and transactions

#### Result Analyzer
- Analyzes query execution results
- Provides insights and explanations
- Generates human-readable summaries

### 3. Utilities (`utils/`)
- Schema Embedder: Handles database schema embedding and similarity search
- Database Configuration: Manages database connections and configurations
- Search Utilities: Provides fuzzy search and matching capabilities
- Schema Files: Contains database schema definitions in JSON and pickle formats

## Workflow

1. **Query Input**
   - User provides natural language query
   - System processes and normalizes input

2. **SQL Generation**
   - Multiple LLMs generate SQL independently
   - Schema context is provided for accurate generation
   - Generated SQL is validated for syntax and structure

3. **Entity Extraction**
   - System extracts entities from generated SQL
   - Identifies tables, columns, and values
   - Validates entity relationships

4. **Value Matching**
   - Matches extracted entities against database
   - Validates entity existence
   - Ensures data consistency

5. **SQL Refinement**
   - Refines SQL based on matching results
   - Optimizes query structure
   - Ensures query efficiency

6. **Query Execution**
   - Executes refined SQL
   - Retrieves results
   - Handles any execution errors

7. **Result Analysis**
   - Analyzes execution results
   - Provides insights
   - Generates summaries

## Setup and Configuration

1. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **API Keys**
   Set the following environment variables:
   - `HUGGINGFACE_API_KEY`
   - `DEEPSEEK_API_KEY`
   - `GEMINI_API_KEY`

3. **Database Configuration**
   - Configure database connection in `utils/db_config.py`
   - Ensure schema is properly embedded using `utils/schema_embedder.py`

## Usage

The system can be used through the Jupyter notebook interface (`workflow_test.ipynb`) or programmatically:

```python
from engine.generator import SQLGenerator
from engine.entity_extractor import EntityExtractor
# ... import other components as needed

# Initialize components
generator = SQLGenerator()
extractor = EntityExtractor()

# Generate SQL
result = generator.main_generator("Your natural language query")

# Extract entities
entities = extractor.main_entity_extractor(result['generated_sql'])
```

## Testing

The system includes comprehensive test suites for each component:
- `engine/*_test.py`: Tests for core engine components
- `utils/*_test.py`: Tests for utility functions
- `llm_config/llm_call_test.py`: Tests for LLM configuration

Run tests using:
```bash
python -m pytest engine/*_test.py utils/*_test.py llm_config/*_test.py
```

## Project Structure

```
.
├── engine/                 # Core SQL generation and processing engine
│   ├── generator.py       # SQL query generation
│   ├── entity_extractor.py # Entity extraction from SQL
│   ├── value_matcher.py   # Value matching utilities
│   ├── refiner.py        # SQL query refinement
│   ├── executor.py       # SQL query execution
│   └── analyzer.py       # Result analysis
├── llm_config/           # LLM configuration and API settings
│   └── llm_call.py      # LLM API interaction utilities
├── utils/               # Utility functions and helpers
│   ├── schema_embedder.py # Schema embedding utilities
│   ├── db_config.py     # Database configuration
│   ├── search.py        # Search utilities
│   ├── db_schema.json   # Database schema definition
│   └── db_schema.pkl    # Embedded schema data
├── workflow_test.ipynb  # Jupyter notebook demonstrating the workflow
└── requirements.txt     # Project dependencies
```

## Dependencies

- Python 3.8 or higher
- PostgreSQL database
- Access to LLM APIs (DeepSeek, Mistral, Gemini)

Key Python packages:
- requests>=2.32.3: HTTP requests for API calls
- python-dotenv>=1.1.0: Environment variable management
- sqlalchemy>=2.0.40: Database ORM
- pandas>=2.2.3: Data manipulation
- sentence-transformers==2.2.2: Schema embeddings
- scikit-learn>=1.4.0: Machine learning utilities
- pytest>=8.0.0: Testing framework

For a complete list of dependencies, see `requirements.txt`.
