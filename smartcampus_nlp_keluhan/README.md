# Smart Campus NLP Complaint Classifier

Judul:
Klasifikasi Kategori dan Prioritas Keluhan Mahasiswa Berbasis Natural Language Processing untuk Mendukung Layanan Smart Campus

## Isi project
- data_keluhan_dummy.csv
- notebook_training.ipynb
- train_model.py
- app.py
- requirements.txt
- models/model_kategori.joblib
- models/model_prioritas.joblib
- hasil_evaluasi_model.csv

## Cara menjalankan

1. Install library:
pip install -r requirements.txt

2. Training model:
python train_model.py

3. Jalankan aplikasi:
streamlit run app.py

Format kolom wajib:
keluhan,kategori,prioritas

Contoh:
WiFi kampus sering mati saat jam kuliah,Jaringan,Tinggi

## Kategori yang disarankan
- Akademik
- Administrasi
- Keuangan
- Jaringan
- Fasilitas
- Kebersihan
- Keamanan

## Prioritas yang disarankan
- Rendah
- Sedang
- Tinggi

## Catatan
Dataset di project ini masih dummy. Gunakan untuk prototype awal, lalu ganti dengan data hasil pengumpulan kelompok.
