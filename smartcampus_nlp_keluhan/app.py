from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


# Konfigurasi halaman harus dipanggil sebelum elemen Streamlit lain
st.set_page_config(
    page_title="Smart Campus NLP",
    page_icon="🎓",
    layout="centered"
)

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "models"
DATA_PATH = BASE_DIR / "data_keluhan_dummy.csv"

MODEL_KATEGORI_PATH = MODEL_DIR / "model_kategori.joblib"
MODEL_PRIORITAS_PATH = MODEL_DIR / "model_prioritas.joblib"


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
    "Tinggi": (
        "Perlu ditangani cepat karena berdampak langsung "
        "pada kegiatan kampus."
    )
}


@st.cache_resource
def load_models():
    """
    Memuat model kategori dan prioritas dari folder models.
    """

    if not MODEL_KATEGORI_PATH.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {MODEL_KATEGORI_PATH}"
        )

    if not MODEL_PRIORITAS_PATH.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {MODEL_PRIORITAS_PATH}"
        )

    model_kategori = joblib.load(MODEL_KATEGORI_PATH)
    model_prioritas = joblib.load(MODEL_PRIORITAS_PATH)

    return model_kategori, model_prioritas


st.title("🎓 Smart Campus Complaint Classifier")

st.write(
    "Aplikasi demo NLP untuk mengklasifikasikan kategori "
    "dan prioritas keluhan mahasiswa."
)


with st.expander("Lihat contoh format data"):
    contoh = pd.DataFrame(
        {
            "keluhan": [
                "WiFi kampus sering mati saat jam kuliah",
                "AC ruang 204 tidak dingin",
                "Pembayaran UKT saya belum terverifikasi"
            ],
            "kategori": [
                "Jaringan",
                "Fasilitas",
                "Keuangan"
            ],
            "prioritas": [
                "Tinggi",
                "Sedang",
                "Tinggi"
            ]
        }
    )

    st.dataframe(
        contoh,
        use_container_width=True,
        hide_index=True
    )


keluhan = st.text_area(
    label="Masukkan keluhan mahasiswa",
    placeholder=(
        "Contoh: WiFi di gedung B sering mati "
        "saat kelas online."
    ),
    height=130,
    key="input_keluhan"
)


col1, col2 = st.columns(2)

with col1:
    prediksi = st.button(
        "Prediksi",
        use_container_width=True,
        type="primary"
    )

with col2:
    reset = st.button(
        "Reset",
        use_container_width=True
    )


if reset:
    st.session_state["input_keluhan"] = ""
    st.rerun()


if prediksi:
    if not keluhan.strip():
        st.warning("Masukkan teks keluhan terlebih dahulu.")

    else:
        try:
            model_kategori, model_prioritas = load_models()

            kategori = model_kategori.predict([keluhan])[0]
            prioritas = model_prioritas.predict([keluhan])[0]

            unit = UNIT_MAP.get(
                kategori,
                "Unit layanan terkait"
            )

            info_prioritas = PRIORITY_INFO.get(
                prioritas,
                "Informasi prioritas belum tersedia."
            )

            st.subheader("Hasil Prediksi")

            st.success(f"Kategori: {kategori}")
            st.info(f"Prioritas: {prioritas}")

            st.write(f"Unit penanganan: {unit}")
            st.write(
                f"Keterangan prioritas: {info_prioritas}"
            )

            st.subheader("Ringkasan")

            st.write(
                f"Keluhan ini masuk kategori {kategori} "
                f"dengan prioritas {prioritas}. "
                f"Sistem merekomendasikan laporan "
                f"diteruskan ke {unit}."
            )

        except FileNotFoundError as error:
            st.error("Model belum ditemukan di server.")

            st.code(str(error))

            st.write(
                "Pastikan folder `models` dan kedua file "
                "model sudah berada di repository GitHub."
            )

        except Exception as error:
            st.error("Terjadi kesalahan saat menjalankan prediksi.")

            st.code(
                f"{type(error).__name__}: {error}"
            )


st.divider()

st.caption(
    "Demo tugas Machine Learning, NLP, dan Smart Campus."
)