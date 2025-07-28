import streamlit as st
import datetime
import pandas as pd

from model import KonsumsiObat
from manajer_obat import ManajerObat
from konfigurasi import WAKTU_MINUM

manajer = ManajerObat()

st.set_page_config(page_title="Monitoring Obat", layout="wide")
st.title("💊 Aplikasi Monitoring Konsumsi Obat")

menu = st.sidebar.radio("Navigasi", ["➕ Tambah Konsumsi", "📋 Riwayat Konsumsi", "📊 Ringkasan Harian"])

st.sidebar.markdown("---")
st.sidebar.markdown("Pemrograman Berbasis Objek")
st.sidebar.markdown("**👤 Nama:** Indra Wijaya")
st.sidebar.markdown("**🆔 NIM:** 4.33.24.0.13")
st.sidebar.markdown("**🏫 Kelas:** TI-1A")

# ➕ HALAMAN TAMBAH OBAT
if menu == "➕ Tambah Konsumsi":
    st.subheader("📝 Tambahkan Catatan Konsumsi Obat")
    col1, col2 = st.columns(2)
    with st.form("form_tambah"):
        with col1:
            nama_obat = st.text_input("Nama Obat *")
            dosis = st.text_input("Dosis (misal: 500mg)")
        with col2:
            waktu = st.selectbox("Waktu Minum", WAKTU_MINUM)
            tanggal = st.date_input("Tanggal", value=datetime.date.today())
        submit = st.form_submit_button("💾 Simpan Data")
        if submit:
            if not nama_obat.strip():
                st.warning("⚠️ Nama obat wajib diisi.")
            else:
                data = KonsumsiObat(nama_obat, dosis, waktu, tanggal)
                if manajer.tambah_konsumsi(data):
                    st.success("✅ Data berhasil disimpan.")
                    st.rerun()
                else:
                    st.error("❌ Gagal menyimpan data.")

# HALAMAN RIWAYAT
elif menu == "📋 Riwayat Konsumsi":
    st.subheader("📜 Riwayat Konsumsi Obat")
    df = manajer.get_dataframe()
    if df.empty:
        st.info("Belum ada data.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("### 🛠️ Edit / Hapus Data")

        id_opsi = st.number_input("Masukkan ID:", min_value=1, step=1)
        aksi = st.radio("Pilih Aksi", ["Edit", "Hapus"], horizontal=True)

        if aksi == "Hapus":
            if st.button("🗑️ Hapus Data"):
                if manajer.hapus_konsumsi(id_opsi):
                    st.success(f"✅ Data ID {id_opsi} dihapus.")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("❌ Gagal menghapus. ID tidak ditemukan.")
        else:
            semua = manajer.get_semua()
            item = next((x for x in semua if x.id == id_opsi), None)
            if item:
                with st.form("form_edit"):
                    nama_obat = st.text_input("Nama Obat", value=item.nama_obat)
                    dosis = st.text_input("Dosis", value=item.dosis)
                    waktu = st.selectbox("Waktu", options=WAKTU_MINUM, index=WAKTU_MINUM.index(item.waktu))
                    tanggal = st.date_input("Tanggal", value=item.tanggal)
                    submit = st.form_submit_button("✅ Simpan Perubahan")
                    if submit:
                        updated = KonsumsiObat(nama_obat, dosis, waktu, tanggal, id_konsumsi=id_opsi)
                        if manajer.update_konsumsi(updated):
                            st.success("✅ Data berhasil diperbarui.")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error("❌ Gagal update data.")
            else:
                st.warning("⚠️ ID tidak ditemukan.")

# HALAMAN RINGKASAN
elif menu == "📊 Ringkasan Harian":
    st.subheader("📈 Ringkasan Konsumsi Harian")
    tanggal = st.date_input("Pilih Tanggal", value=datetime.date.today())
    ringkasan = manajer.ringkasan_harian(tanggal)

    if not ringkasan:
        st.info("Tidak ada konsumsi obat pada tanggal ini.")
    else:
        df_ringkasan = pd.DataFrame(ringkasan.items(), columns=["Obat", "Jumlah"])
        col1, col2 = st.columns(2)
        with col1:
            st.write("Tabel Konsumsi:")
            st.dataframe(df_ringkasan, hide_index=True)
        with col2:
            st.write("Grafik Konsumsi:")
            st.bar_chart(df_ringkasan.set_index("Obat"))
