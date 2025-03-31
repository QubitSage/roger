import sqlite3
import pandas as pd
import json

# Connect to the database
conn = sqlite3.connect("dados (2).db")
cursor = conn.cursor()

# Get list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

db_info = {
    "tables": [],
}

# For each table, get the schema and a sample of data
for table in tables:
    table_name = table[0]
    table_info = {
        "name": table_name,
        "schema": [],
        "sample_data": []
    }
    
    # Get schema
    cursor.execute(f"PRAGMA table_info({table_name})")
    schema = cursor.fetchall()
    for column in schema:
        table_info["schema"].append({
            "name": column[1],
            "type": column[2]
        })
    
    # Get sample data
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
    sample_data = cursor.fetchall()
    if sample_data:
        column_names = [description[0] for description in cursor.description]
        for row in sample_data:
            row_dict = {}
            for i, value in enumerate(row):
                row_dict[column_names[i]] = value
            table_info["sample_data"].append(row_dict)
    
    db_info["tables"].append(table_info)

conn.close()

# Save to file
with open("db_info.json", "w") as f:
    json.dump(db_info, f, indent=2) 