# SkillAggregator Project Index

## Project Structure Overview

### Root Directory
- `SkillAggregator/`: Main project root directory

### Core Directories
1. **`engine/`**: Core processing components
   - `metadata.py`: Defines data structures and metadata for learning analytics
   - `decomposer.py`: Breaks down complex queries into manageable sub-queries
   - `generator.py`: Converts natural language queries to SQL
   - `executor.py`: Executes and validates SQL queries
   - `analyzer.py`: Provides insights and analysis from query results
   - `orchestrator.py`: Coordinates the entire query processing workflow

2. **`testing/`**: Testing and validation components
   - `test_workflow.py`: End-to-end workflow testing
   - `test_decomposer.py`: Testing query decomposition functionality
   - `test_generator.py`: Testing SQL generation
   - `test_analyzer.py`: Testing result analysis
   - `test_ui.py`: User interface testing
   - `test_cases.md`: Comprehensive test scenarios
   - `test_search.py`: Entity search and matching tests

3. **`utils/`**: Utility functions and helpers
   - `search.py`: Advanced search and entity matching
   - Other utility modules for text processing, etc.

4. **`config/`**: Configuration management
   - `config.py`: Central configuration settings

### Documentation Files
- `Documentation.md`: Comprehensive project documentation
- `Index.md`: Current file - project structure overview

### Configuration and Setup
- `requirements.txt`: Project dependencies
- `.env`: Environment configuration (not tracked in version control)
- `pyproject.toml`: Project build and tool configuration

### Potential Future Directories
- `models/`: Machine learning models
- `integrations/`: External service integrations
- `scripts/`: Utility scripts for setup/maintenance

## File Purposes Breakdown

### Engine Components
- `metadata.py`: 
  - Defines data structures for learning analytics
  - Provides metadata for tables and columns
  - Supports dynamic query processing

- `decomposer.py`:
  - Breaks complex queries into sub-queries
  - Uses LLM for intelligent query understanding
  - Extracts relevant entities from queries

- `generator.py`:
  - Converts natural language to SQL
  - Ensures query safety and relevance
  - Uses table metadata for precise query generation

- `analyzer.py`:
  - Provides insights from query results
  - Generates structured analysis
  - Uses LLM for comprehensive interpretation

- `orchestrator.py`:
  - Coordinates entire query workflow
  - Manages state and error handling
  - Integrates all engine components

### Testing Components
- Comprehensive test coverage for each engine component
- Validates query decomposition, generation, and analysis
- Provides test cases for various scenarios

### Utility Components
- Advanced search and matching algorithms
- Text processing utilities
- Helper functions for core components

## Technology Stack
- Language: Python 3.9+
- LLM: Anthropic Claude (Haiku/Sonnet)
- Database: SQLite
- Libraries: 
  - LangChain
  - LangGraph
  - scikit-learn
  - pandas
  - numpy

## Key Workflows
1. Query Decomposition
2. Entity Extraction
3. SQL Generation
4. Query Execution
5. Results Analysis

## Contribution Guidelines
- Follow PEP 8 style guide
- Write comprehensive tests
- Document new features
- Maintain modular architecture

## Future Roadmap
- Enhanced machine learning integration
- More sophisticated query understanding
- Expanded metadata support
- Improved error handling and recovery
