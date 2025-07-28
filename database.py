import sqlite3
import pandas as pd
from konfigurasi import DB_PATH

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, params=()):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        print(f"[DB ERROR] {e}")
        return None
    finally:
        conn.close()

def fetch_query(query, params=()):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()

def get_dataframe(query, params=()):
    conn = get_db_connection()
    try:
        return pd.read_sql_query(query, conn, params=params)
    except:
        return pd.DataFrame()
    finally:
        conn.close()
