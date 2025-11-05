import sqlite3
import pandas as pd
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path: str = "data/gtis.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                date DATE NOT NULL,
                interest_value REAL NOT NULL,
                geo TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(keyword, date, geo)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                prediction_date DATE NOT NULL,
                predicted_value REAL NOT NULL,
                model_name TEXT NOT NULL,
                confidence_lower REAL,
                confidence_upper REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store_trends(self, data: pd.DataFrame, keywords: list):
        conn = sqlite3.connect(self.db_path)
        for keyword in keywords:
            if keyword in data.columns:
                df = data[[keyword]].reset_index()
                df.columns = ['date', 'interest_value']
                df['keyword'] = keyword
                df['geo'] = ''
                
                for _, row in df.iterrows():
                    conn.execute("""
                        INSERT OR REPLACE INTO trends (keyword, date, interest_value, geo)
                        VALUES (?, ?, ?, ?)
                    """, (row['keyword'], row['date'], row['interest_value'], row['geo']))
        conn.commit()
        conn.close()
    
    def get_trend_history(self, keyword: str, days: int = 365):
        conn = sqlite3.connect(self.db_path)
        query = """
            SELECT date, interest_value
            FROM trends
            WHERE keyword = ?
            ORDER BY date DESC
            LIMIT ?
        """
        df = pd.read_sql_query(query, conn, params=(keyword, days))
        conn.close()
        
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date').sort_index()
        return df
    
    def check_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.close()
            return True
        except:
            return False
