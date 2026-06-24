from pathlib import Path
import re
import string

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


UNIT_MAP = {
    "Akademik": "Program Studi / Jurusan",
    "Administrasi": "BAAK / Administrasi Fakultas",
    "Keuangan": "BPPK / Bagian Keuangan",
    "Jaringan": "UPT TIK / Tim Jaringan",
    "Fasilitas": "Sarana dan Prasarana",
    "Kebersihan": "Sarana dan Prasarana",
    "Keamanan": "Satpam / Unit Keamanan Kampus",
}


CATEGORY_ICON = {
    "Akademik": "📚",
    "Administrasi": "📄",
    "Keuangan": "💳",
    "Jaringan": "📡",
    "Fasilitas": "🏫",
    "Kebersihan": "🧹",
    "Keamanan": "🛡️",
}


PRIORITY_ICON = {
    "Rendah": "🟢",
    "Sedang": "🟡",
    "Tinggi": "🔴",
}


PRIORITY_INFO = {
    "Rendah": "Keluhan dapat ditangani sesuai antrean layanan.",
    "Sedang": "Keluhan perlu ditindaklanjuti karena mulai mengganggu aktivitas.",
    "Tinggi": "Keluhan perlu segera ditangani karena berdampak langsung pada kegiatan kampus.",
}


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_dataset(data_path):
    data_path = Path(data_path)

    if not data_path.exists():
        return pd.DataFrame(columns=["keluhan", "kategori", "prioritas"])

    data = pd.read_csv(data_path)
    data.columns = [col.strip().lower().replace(" ", "_") for col in data.columns]

    rename_map = {
        "teks_keluhan": "keluhan",
        "kategori_keluhan": "kategori",
        "prioritas_keluhan": "prioritas",
    }

    data = data.rename(columns=rename_map)

    return data


def load_priority_model(model_path):
    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(f"Model prioritas tidak ditemukan: {model_path}")

    return joblib.load(model_path)


def train_category_model(data):
    if data.empty:
        return None

    if "keluhan" not in data.columns or "kategori" not in data.columns:
        return None

    model_data = data.dropna(subset=["keluhan", "kategori"]).copy()

    if model_data.empty:
        return None

    if model_data["kategori"].nunique() < 2:
        return None

    model_data["clean_text"] = model_data["keluhan"].apply(clean_text)

    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(max_features=3000, ngram_range=(1, 2))),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )

    pipeline.fit(model_data["clean_text"], model_data["kategori"])

    return pipeline


def fallback_category(text):
    text = clean_text(text)

    keyword_map = {
        "Jaringan": ["wifi", "internet", "jaringan", "sinyal", "login", "lemot", "lambat", "terputus"],
        "Fasilitas": ["ac", "proyektor", "kursi", "meja", "speaker", "ruang", "gedung", "lampu", "rusak"],
        "Keuangan": ["ukt", "bayar", "pembayaran", "tagihan", "bppk", "keuangan", "semester"],
        "Akademik": ["krs", "khs", "nilai", "jadwal", "kuliah", "ujian", "dosen", "akademik"],
        "Administrasi": ["surat", "legalisir", "administrasi", "baak", "dokumen", "data", "pengajuan"],
        "Kebersihan": ["toilet", "sampah", "kotor", "bersih", "bau", "licin", "debu"],
        "Keamanan": ["parkir", "helm", "hilang", "cctv", "satpam", "gelap", "keamanan"],
    }

    for category, keywords in keyword_map.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "Administrasi"


def normalize_category(label):
    label = str(label).strip()

    aliases = {
        "jaringan internet": "Jaringan",
        "internet": "Jaringan",
        "sarana": "Fasilitas",
        "sarana prasarana": "Fasilitas",
        "fasilitas kampus": "Fasilitas",
        "administrasi akademik": "Administrasi",
        "keuangan kampus": "Keuangan",
        "keamanan kampus": "Keamanan",
    }

    lower_label = label.lower()

    if lower_label in aliases:
        return aliases[lower_label]

    for category in UNIT_MAP.keys():
        if category.lower() == lower_label:
            return category

    return label


def normalize_priority(label):
    label = str(label).strip()

    lower_label = label.lower()

    if lower_label in ["0", "rendah", "low"]:
        return "Rendah"

    if lower_label in ["1", "sedang", "medium"]:
        return "Sedang"

    if lower_label in ["2", "tinggi", "high"]:
        return "Tinggi"

    for priority in PRIORITY_INFO.keys():
        if priority.lower() == lower_label:
            return priority

    return label


def predict_from_model(model_artifact, text):
    cleaned_text = clean_text(text)

    if hasattr(model_artifact, "predict"):
        try:
            return model_artifact.predict([cleaned_text])[0]
        except Exception:
            return model_artifact.predict([text])[0]

    if isinstance(model_artifact, dict):
        vectorizer = (
            model_artifact.get("vectorizer")
            or model_artifact.get("tfidf")
            or model_artifact.get("tfidf_vectorizer")
        )

        classifier = (
            model_artifact.get("model")
            or model_artifact.get("classifier")
            or model_artifact.get("clf")
        )

        if vectorizer is not None and classifier is not None:
            transformed_text = vectorizer.transform([cleaned_text])
            return classifier.predict(transformed_text)[0]

    if isinstance(model_artifact, (list, tuple)) and len(model_artifact) >= 2:
        vectorizer = model_artifact[0]
        classifier = model_artifact[1]

        if hasattr(vectorizer, "transform") and hasattr(classifier, "predict"):
            transformed_text = vectorizer.transform([cleaned_text])
            return classifier.predict(transformed_text)[0]

    raise TypeError("Format model tidak dikenali oleh aplikasi.")


def predict_keluhan(text, data, priority_model, category_model):
    if not text.strip():
        raise ValueError("Keluhan masih kosong.")

    cleaned_text = clean_text(text)

    if category_model is not None:
        kategori = category_model.predict([cleaned_text])[0]
    else:
        kategori = fallback_category(text)

    prioritas = predict_from_model(priority_model, text)

    kategori = normalize_category(kategori)
    prioritas = normalize_priority(prioritas)

    unit = UNIT_MAP.get(kategori, "Unit layanan terkait")

    return {
        "keluhan": text,
        "kategori": kategori,
        "prioritas": prioritas,
        "unit": unit,
        "category_icon": CATEGORY_ICON.get(kategori, "📌"),
        "priority_icon": PRIORITY_ICON.get(prioritas, "⚪"),
        "priority_info": PRIORITY_INFO.get(prioritas, "Informasi prioritas belum tersedia."),
    }