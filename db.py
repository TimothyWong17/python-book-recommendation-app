import os
import sqlite3
import pandas as pd

class DB:
    def __init__(self,db_path):
        self.conn = sqlite3.connect(db_path)
        
    def get_table_data(self, table_name):
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
        return df
        
    def adhoc_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    
    def table_stats(self, table_name):
        cur = self.conn.cursor()
        cur.execute(f"""
                    PRAGMA table_info({table_name})
                    """)
        rows = cur.fetchall()
        for row in rows:
            print(row)