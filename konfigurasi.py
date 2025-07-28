# konfigurasi.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'konsumsi_obat.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

# Waktu minum yang umum
WAKTU_MINUM = ["Pagi", "Siang", "Sore", "Malam"]