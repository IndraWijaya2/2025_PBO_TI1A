import datetime
import pandas as pd
from model import KonsumsiObat
import database

class ManajerObat:
    def tambah_konsumsi(self, konsumsi: KonsumsiObat) -> bool:
        query = "INSERT INTO konsumsi (nama_obat, dosis, waktu, tanggal) VALUES (?, ?, ?, ?)"
        params = (konsumsi.nama_obat, konsumsi.dosis, konsumsi.waktu, konsumsi.tanggal.strftime("%Y-%m-%d"))
        return database.execute_query(query, params) > 0

    def hapus_konsumsi(self, id_konsumsi: int) -> bool:
        return database.execute_query("DELETE FROM konsumsi WHERE id = ?", (id_konsumsi,)) > 0

    def update_konsumsi(self, konsumsi: KonsumsiObat) -> bool:
        query = "UPDATE konsumsi SET nama_obat=?, dosis=?, waktu=?, tanggal=? WHERE id=?"
        params = (konsumsi.nama_obat, konsumsi.dosis, konsumsi.waktu, konsumsi.tanggal.strftime("%Y-%m-%d"), konsumsi.id)
        return database.execute_query(query, params) > 0

    def get_dataframe(self, tanggal: datetime.date | None = None) -> pd.DataFrame:
        query = "SELECT * FROM konsumsi"
        params = ()
        if tanggal:
            query += " WHERE tanggal = ?"
            params = (tanggal.strftime("%Y-%m-%d"),)
        query += " ORDER BY tanggal DESC"
        df = database.get_dataframe(query, params)
        if not df.empty:
            df.rename(columns={
                'id': 'ID',
                'nama_obat': 'Nama Obat',
                'dosis': 'Dosis',
                'waktu': 'Waktu',
                'tanggal': 'Tanggal'
            }, inplace=True)
        return df

    def get_semua(self):
        rows = database.fetch_query("SELECT * FROM konsumsi ORDER BY tanggal DESC")
        return [KonsumsiObat(**dict(row)) for row in rows] if rows else []
    
    def ringkasan_harian(self, tanggal: datetime.date) -> dict:
        query = "SELECT nama_obat, COUNT(*) as jumlah FROM konsumsi WHERE tanggal = ? GROUP BY nama_obat"
        params = (tanggal.strftime("%Y-%m-%d"),)
        rows = database.fetch_query(query, params)
        hasil = {}
        if rows:
            for row in rows:
                hasil[row["nama_obat"]] = row["jumlah"]
        return hasil

