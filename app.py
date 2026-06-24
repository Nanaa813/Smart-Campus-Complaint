from pathlib import Path

import streamlit as st

from backend.predictor import (
    load_dataset,
    load_priority_model,
    predict_keluhan,
    train_category_model,
)

from frontend.components import (
    input_helper,
    render_about,
    render_flow,
    render_footer,
    render_hero,
    render_result,
    render_unit_mapping,
    section_title,
)

from frontend.styles import get_css


st.set_page_config(
    page_title="E-Complaint Smart Campus",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "data_keluhan.csv"
MODEL_PATH = BASE_DIR / "models" / "model_prioritas_keluhan.pkl"


st.markdown(get_css(), unsafe_allow_html=True)


@st.cache_data
def get_data():
    return load_dataset(DATA_PATH)


@st.cache_resource
def get_priority_model():
    return load_priority_model(MODEL_PATH)


@st.cache_resource
def get_category_model():
    data = load_dataset(DATA_PATH)
    return train_category_model(data)


def set_example(text):
    st.session_state["input_keluhan"] = text


def clear_input():
    st.session_state["input_keluhan"] = ""


if "input_keluhan" not in st.session_state:
    st.session_state["input_keluhan"] = ""


data_keluhan = get_data()

render_hero()

tabs = st.tabs(
    [
        "✨ Prediksi Keluhan",
        "⚙️ Alur Sistem",
        "ℹ️ Tentang Sistem",
    ]
)


with tabs[0]:
    section_title(
        "Prediksi Keluhan Mahasiswa",
        "Tulis keluhan yang ingin disampaikan. Sistem akan memprediksi kategori, tingkat prioritas, dan unit kampus yang sesuai untuk menangani keluhan tersebut.",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button(
            "📡 WiFi lambat",
            use_container_width=True,
            on_click=set_example,
            args=("WiFi kampus lambat dan sering terputus saat jam kuliah online.",),
        )

    with col2:
        st.button(
            "🏫 Fasilitas rusak",
            use_container_width=True,
            on_click=set_example,
            args=("Proyektor di ruang kelas tidak bisa digunakan saat presentasi.",),
        )

    with col3:
        st.button(
            "💳 UKT bermasalah",
            use_container_width=True,
            on_click=set_example,
            args=("Pembayaran UKT saya belum terverifikasi di sistem.",),
        )

    input_helper()

    keluhan = st.text_area(
        "Kolom keluhan mahasiswa",
        placeholder="Tulis keluhan di sini...",
        height=155,
        key="input_keluhan",
    )

    button_col1, button_col2 = st.columns(2)

    with button_col1:
        prediksi = st.button(
            "✨ Prediksi Keluhan",
            use_container_width=True,
            type="primary",
        )

    with button_col2:
        st.button(
            "↻ Reset",
            use_container_width=True,
            on_click=clear_input,
        )

    if prediksi:
        if not keluhan.strip():
            st.warning("Silakan tuliskan keluhan terlebih dahulu.")

        else:
            try:
                priority_model = get_priority_model()
                category_model = get_category_model()

                result = predict_keluhan(
                    text=keluhan,
                    data=data_keluhan,
                    priority_model=priority_model,
                    category_model=category_model,
                )

                render_result(result)

            except FileNotFoundError as error:
                st.error("Model belum ditemukan.")
                st.info("Pastikan file model .pkl sudah berada di folder models pada repository.")
                st.code(str(error))

            except Exception as error:
                st.error("Terjadi kesalahan saat menjalankan prediksi.")
                st.info("Cek kembali format model dan struktur file project.")
                st.code(f"{type(error).__name__}: {error}")


with tabs[1]:
    section_title(
        "Alur Sistem",
        "Sistem membaca teks keluhan, memproses teks, menjalankan model prediksi, lalu memberikan rekomendasi unit penanganan.",
    )

    render_flow()
    render_unit_mapping()


with tabs[2]:
    section_title(
        "Tentang Sistem",
        "Informasi singkat tentang tujuan aplikasi dan kontribusi project.",
    )

    render_about()


render_footer()