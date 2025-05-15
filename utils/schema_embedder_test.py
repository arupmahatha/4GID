import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.schema_embedder import SchemaEmbedder

# Paths relative to project root
SCHEMA_JSON = os.path.join(project_root, 'utils', 'db_schema.json')
DB_SCHEMA = os.path.join(project_root, 'utils', 'db_schema.pkl')

# Example test queries
TEST_QUERIES = [
    "Who all have admin permissions?"
]

def main():
    embedder = SchemaEmbedder()
    # Create db_schema if not present
    if not os.path.exists(DB_SCHEMA):
        print("Creating vector database...")
        embedder.create_db_schema(SCHEMA_JSON, DB_SCHEMA)
        print("Vector database created.")
    else:
        print("Vector database already exists.")

    for query in TEST_QUERIES:
        print(f"\nQuery: {query}\n")
        results = embedder.query_tables(query, DB_SCHEMA, k=10)
        for table_name, columns in results:
            print(f"Table: {table_name}")
            for col in columns:
                print(f"  - {col}")

if __name__ == "__main__":
    main()
