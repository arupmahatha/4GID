import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

class SchemaEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def create_db_schema(self, schema_json_path, db_schema_path):
        with open(schema_json_path, 'r') as f:
            schema_data = json.load(f)
        # Support both {"db_schema": [...]} and [...] at root
        if isinstance(schema_data, dict) and 'db_schema' in schema_data:
            schema = schema_data['db_schema']
        else:
            schema = schema_data
        embeddings_dict = {}
        for table in schema:
            table_text = self._table_to_text(table)
            embedding = self.model.encode(table_text)
            # Support both 'name' and 'table_name' as table name key
            table_name = table.get('name') or table.get('table_name')
            columns = [col.get('name') for col in table.get('columns', [])]
            embeddings_dict[table_name] = {
                'embedding': embedding,
                'columns': columns,
                'table': table
            }
        with open(db_schema_path, 'wb') as f:
            pickle.dump(embeddings_dict, f)

    def query_tables(self, query, db_schema_path, k=10):
        with open(db_schema_path, 'rb') as f:
            embeddings_dict = pickle.load(f)
        table_names = list(embeddings_dict.keys())
        table_embeddings = np.array([embeddings_dict[name]['embedding'] for name in table_names])
        query_embedding = self.model.encode(query)
        similarities = cosine_similarity([query_embedding], table_embeddings)[0]
        top_indices = similarities.argsort()[::-1][:k]
        results = []
        for idx in top_indices:
            name = table_names[idx]
            columns = embeddings_dict[name]['columns']
            results.append((name, columns))
        return results

    def _table_to_text(self, table):
        table_name = table.get('name') or table.get('table_name')
        text = f"Table: {table_name}\nDescription: {table.get('description', '')}\n"
        for col in table.get('columns', []):
            col_desc = col.get('description', '')
            col_type = col.get('type', '')
            choices = col.get('choices', None)
            col_name = col.get('name')
            text += f"Column: {col_name} ({col_type}) - {col_desc}"
            if choices:
                text += f" Choices: {', '.join(map(str, choices))}"
            text += "\n"
        return text

if __name__ == "__main__":
    SCHEMA_JSON = os.path.join(os.path.dirname(__file__), 'db_schema.json')
    DB_SCHEMA = os.path.join(os.path.dirname(__file__), 'db_schema.pkl')
    embedder = SchemaEmbedder()
    print(f"Creating vector database from {SCHEMA_JSON} ...")
    embedder.create_db_schema(SCHEMA_JSON, DB_SCHEMA)
    print(f"Vector database created at {DB_SCHEMA}.") 