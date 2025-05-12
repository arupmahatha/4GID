from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from urllib.parse import quote_plus
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration from environment variables
DB_CONFIG = {
    'client': os.getenv('DB_CLIENT', 'postgres'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'database': os.getenv('DB_NAME'),
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

# Validate required environment variables
required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Create SQLAlchemy engine with read-only mode
# URL encode the password to handle special characters
encoded_password = quote_plus(DB_CONFIG['password'])
DATABASE_URL = f"postgresql://{DB_CONFIG['username']}:{encoded_password}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Create engine with read-only mode
engine = create_engine(
    DATABASE_URL,
    connect_args={'options': '-c default_transaction_read_only=on'}
)

# Create session factory with read-only mode
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create base class for models
Base = declarative_base()

def is_read_only_query(query):
    """
    Check if the query is read-only
    """
    query = query.lower().strip()
    # List of SQL commands that modify data
    modifying_commands = [
        'insert', 'update', 'delete', 'drop', 'create', 'alter', 'truncate',
        'grant', 'revoke', 'commit', 'rollback'
    ]
    return not any(cmd in query for cmd in modifying_commands)

def is_valid_table_name(table_name):
    """
    Validate table name to prevent SQL injection
    """
    # Only allow alphanumeric characters, underscores, and dots
    return bool(re.match(r'^[a-zA-Z0-9_.]+$', table_name))

def get_db():
    """
    Get database session (read-only)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def execute_query(query, params=None):
    """
    Execute a raw SQL query and return results (read-only)
    """
    if not is_read_only_query(query):
        raise ValueError("Only SELECT queries are allowed for security reasons")
    
    with engine.connect() as connection:
        result = connection.execute(text(query), params or {})
        return result.fetchall()

def execute_query_pandas(query, params=None):
    """
    Execute a query and return results as pandas DataFrame (read-only)
    """
    if not is_read_only_query(query):
        raise ValueError("Only SELECT queries are allowed for security reasons")
    
    import pandas as pd
    return pd.read_sql_query(text(query), engine, params=params) 