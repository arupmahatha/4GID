from db_config import execute_query, execute_query_pandas
import pandas as pd
import json
import os

def test_connection():
    """Test basic database connection"""
    try:
        result = execute_query("SELECT 1 as test")
        print("✅ Database connection successful!")
        print(f"Test query result: {result}")
        return True
    except Exception as e:
        print("❌ Database connection failed!")
        print(f"Error: {str(e)}")
        return False

def get_table_info():
    """Get information about all tables in the database"""
    query = """
    SELECT 
        table_name,
        table_schema
    FROM information_schema.tables 
    WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
    ORDER BY table_schema, table_name;
    """
    return execute_query_pandas(query)

def get_table_columns(table_name):
    """Get column information for a specific table"""
    query = """
    SELECT 
        column_name,
        data_type,
        character_maximum_length,
        column_default,
        is_nullable
    FROM information_schema.columns
    WHERE table_name = :table_name
    ORDER BY ordinal_position;
    """
    return execute_query_pandas(query, {'table_name': table_name})

def get_sample_data(table_name, limit=5):
    """Get sample data from a specific table"""
    query = f"""
    SELECT * FROM {table_name}
    LIMIT :limit
    """
    return execute_query_pandas(query, {'limit': limit})

def generate_schema_dump():
    """Generate a complete database schema dump and save it as JSON"""
    try:
        # Get all tables
        tables_df = get_table_info()
        
        schema_info = {
            "database_schema": []
        }
        
        for _, table_row in tables_df.iterrows():
            table_name = table_row['table_name']
            
            # Get column information
            columns_df = get_table_columns(table_name)
            
            # Create table info dictionary
            table_info = {
                "table_name": table_name,
                "columns": []
            }
            
            # Add column information
            for _, col_row in columns_df.iterrows():
                column_info = {
                    "name": col_row['column_name'],
                    "type": col_row['data_type'],
                    "nullable": col_row['is_nullable'],
                    "default": col_row['column_default'] if col_row['column_default'] else None
                }
                table_info["columns"].append(column_info)
            
            schema_info["database_schema"].append(table_info)
        
        # Save to file in utils folder
        output_path = os.path.join(os.path.dirname(__file__), 'database_schema.json')
        with open(output_path, 'w') as f:
            json.dump(schema_info, f, indent=2)
        
        print(f"✅ Schema dump saved to '{output_path}'")
        return True
    except Exception as e:
        print("❌ Failed to generate schema dump!")
        print(f"Error: {str(e)}")
        return False

def main():
    # Test connection
    if not test_connection():
        return

    print("\n📊 Database Tables Information:")
    tables_df = get_table_info()
    print(tables_df)
    
    # If we have tables, show more detailed information
    if not tables_df.empty:
        # Get first table for demonstration
        first_table = tables_df.iloc[0]['table_name']
        
        print(f"\n📋 Columns in table '{first_table}':")
        columns_df = get_table_columns(first_table)
        print(columns_df)
        
        print(f"\n📝 Sample data from '{first_table}':")
        sample_df = get_sample_data(first_table)
        print(sample_df)
        
    # Generate schema dump
    generate_schema_dump()

if __name__ == "__main__":
    main()