import datetime

class KonsumsiObat:
    def __init__(self, nama_obat, dosis, waktu, tanggal, id=None):
        self.id = id
        self.nama_obat = nama_obat.strip()
        self.dosis = dosis.strip()
        self.waktu = waktu
        if isinstance(tanggal, str):
            self.tanggal = datetime.datetime.strptime(tanggal, "%Y-%m-%d").date()
        else:
            self.tanggal = tanggal
