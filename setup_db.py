import sqlite3
from konfigurasi import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS konsumsi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_obat TEXT NOT NULL,
    dosis TEXT,
    waktu TEXT,
    tanggal DATE NOT NULL
)
""")
conn.commit()
conn.close()
