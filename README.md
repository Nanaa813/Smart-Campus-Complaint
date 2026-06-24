# E-Complaint Smart Campus

Aplikasi web untuk klasifikasi keluhan mahasiswa berbasis Natural Language Processing.

Repo: e-complaint

## Fokus Aplikasi

Project ini berfokus pada bagian Software Engineering, yaitu:
- Integrasi model Machine Learning dari tim model
- Dashboard dataset keluhan
- Prediksi kategori keluhan
- Prediksi prioritas keluhan
- Rekomendasi unit penanganan
- Tampilan web berbasis Streamlit
- Deployment online

## Model

Model prioritas menggunakan file dari tim Machine Learning:

```text
models/model_prioritas_keluhan.pkl
```

Model tersebut berbentuk pipeline TF-IDF + Linear SVM.

## Struktur Folder

```text
e-complaint/
├── app.py
├── requirements.txt
├── README.md
├── ML_KEL_10.ipynb
├── data/
│   ├── data_keluhan.csv
│   └── hasil_evaluasi_model.csv
└── models/
    ├── model_prioritas_keluhan.pkl
    └── model_prioritas_keluhan2.pkl
```

## Cara Menjalankan Lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy ke Streamlit Cloud

Main file path:

```text
app.py
```

Jika file berada di dalam folder tambahan, gunakan:

```text
e-complaint/app.py
```

## Catatan

Aplikasi ini memakai model prioritas dari tim Machine Learning. Untuk prediksi kategori, aplikasi membuat model kategori dari dataset yang tersedia agar fitur tetap sesuai dengan poster dan alur sistem.
