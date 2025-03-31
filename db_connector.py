import sqlite3
import pandas as pd

class DatabaseConnector:
    def __init__(self, db_path="dados (2).db"):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to the SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def disconnect(self):
        """Disconnect from the SQLite database"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def execute_query(self, query):
        """Execute a SQL query and return the results as a pandas DataFrame"""
        if not self.conn:
            self.connect()
        
        try:
            df = pd.read_sql_query(query, self.conn)
            return df
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
    
    def get_tables(self):
        """Get list of tables in the database"""
        if not self.conn:
            self.connect()
        
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        cursor = self.conn.cursor()
        cursor.execute(query)
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    
    def get_table_schema(self, table_name):
        """Get schema for a specific table"""
        if not self.conn:
            self.connect()
        
        query = f"PRAGMA table_info({table_name})"
        cursor = self.conn.cursor()
        cursor.execute(query)
        schema = cursor.fetchall()
        
        columns = []
        for col in schema:
            columns.append({
                "name": col[1],
                "type": col[2]
            })
        
        return columns
    
    def get_sample_data(self, table_name, limit=5):
        """Get sample data from a table"""
        if not self.conn:
            self.connect()
        
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return self.execute_query(query)
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect() 