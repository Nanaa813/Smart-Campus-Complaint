import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(
    page_title="Smart Campus NLP",
    page_icon="🎓",
    layout="centered"
)

MODEL_DIR = Path("models")
DATA_PATH = Path("data_keluhan_dummy.csv")

UNIT_MAP = {
    "Akademik": "Program Studi / Bagian Akademik",
    "Administrasi": "BAAK / Administrasi Fakultas",
    "Keuangan": "Bagian Keuangan",
    "Jaringan": "UPT TIK / Tim Jaringan",
    "Fasilitas": "Sarana dan Prasarana",
    "Kebersihan": "Petugas Kebersihan / Sarpras",
    "Keamanan": "Satpam / Unit Keamanan Kampus"
}

PRIORITY_INFO = {
    "Rendah": "Bisa ditangani sesuai antrean layanan.",
    "Sedang": "Perlu ditindaklanjuti karena mulai mengganggu aktivitas.",
    "Tinggi": "Perlu ditangani cepat karena berdampak langsung pada kegiatan kampus."
}

@st.cache_resource
def load_models():
    model_kategori = joblib.load(MODEL_DIR / "model_kategori.joblib")
    model_prioritas = joblib.load(MODEL_DIR / "model_prioritas.joblib")
    return model_kategori, model_prioritas

st.title("🎓 Smart Campus Complaint Classifier")
st.write("Aplikasi demo NLP untuk mengklasifikasikan kategori dan prioritas keluhan mahasiswa.")

with st.expander("Lihat contoh format data"):
    contoh = pd.DataFrame({
        "keluhan": [
            "WiFi kampus sering mati saat jam kuliah",
            "AC ruang 204 tidak dingin",
            "Pembayaran UKT saya belum terverifikasi"
        ],
        "kategori": ["Jaringan", "Fasilitas", "Keuangan"],
        "prioritas": ["Tinggi", "Sedang", "Tinggi"]
    })
    st.dataframe(contoh, use_container_width=True)

keluhan = st.text_area(
    "Masukkan keluhan mahasiswa",
    placeholder="Contoh: WiFi di gedung B sering mati saat kelas online.",
    height=130
)

col1, col2 = st.columns(2)
with col1:
    prediksi = st.button("Prediksi", use_container_width=True)
with col2:
    reset = st.button("Reset", use_container_width=True)

if reset:
    st.rerun()

if prediksi:
    if not keluhan.strip():
        st.warning("Masukkan teks keluhan dulu.")
    else:
        try:
            model_kategori, model_prioritas = load_models()

            kategori = model_kategori.predict([keluhan])[0]
            prioritas = model_prioritas.predict([keluhan])[0]

            unit = UNIT_MAP.get(kategori, "Unit terkait")
            info_prioritas = PRIORITY_INFO.get(prioritas, "-")

            st.subheader("Hasil Prediksi")
            st.success(f"Kategori: {kategori}")
            st.info(f"Prioritas: {prioritas}")
            st.write(f"Unit penanganan: {unit}")
            st.write(f"Keterangan prioritas: {info_prioritas}")

            st.subheader("Ringkasan")
            st.write(
                f"Keluhan ini masuk kategori {kategori} dengan prioritas {prioritas}. "
                f"Sistem merekomendasikan laporan diteruskan ke {unit}."
            )

        except FileNotFoundError:
            st.error("Model belum ditemukan. Jalankan dulu: python train_model.py")

st.divider()
st.caption("Demo tugas Machine Learning, NLP, Smart Campus.")
