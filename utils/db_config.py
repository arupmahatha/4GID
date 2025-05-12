from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from urllib.parse import quote_plus
import re

# Database configuration
DB_CONFIG = {
    'client': 'postgres',
    'host': '3.111.123.209',
    'port': 5432,
    'database': 'poims',
    'username': 'devadmin',
    'password': '4gid@2007'
}

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