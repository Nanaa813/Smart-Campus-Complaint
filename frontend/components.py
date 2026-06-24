import html
import textwrap

import streamlit as st


def render_html(markup):
    clean_markup = textwrap.dedent(markup).strip()
    st.html(clean_markup)


def render_hero():
    render_html(
        """
        <div class="hero-card">
            <h1 class="hero-title">🎓 E-Complaint Smart Campus</h1>
            <p class="hero-subtitle">
                Sistem berbasis Natural Language Processing untuk membantu mahasiswa
                mengirimkan keluhan dan mendapatkan rekomendasi unit penanganan
                secara cepat, rapi, dan terarah.
            </p>
            <div class="chip-row">
                <span class="chip">💬 Klasifikasi Keluhan</span>
                <span class="chip">⚡ Prediksi Prioritas</span>
                <span class="chip">🏢 Rekomendasi Unit</span>
                <span class="chip">🏫 Smart Campus</span>
            </div>
        </div>
        """
    )


def section_title(title, description):
    title = html.escape(str(title))
    description = html.escape(str(description))

    render_html(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-desc">{description}</div>
        """
    )


def input_helper():
    render_html(
        """
        <div class="input-helper">
            Klik kolom input di bawah ini, lalu tuliskan keluhan secara singkat dan jelas.
            Contoh: <strong>WiFi di gedung B sering mati saat kelas online.</strong>
        </div>
        """
    )


def render_result(result):
    kategori = html.escape(str(result["kategori"]))
    prioritas = html.escape(str(result["prioritas"]))
    unit = html.escape(str(result["unit"]))
    category_icon = html.escape(str(result["category_icon"]))
    priority_icon = html.escape(str(result["priority_icon"]))
    priority_info = html.escape(str(result["priority_info"]))

    render_html(
        f"""
        <div class="result-wrapper">
            <div class="section-title">Hasil Prediksi</div>

            <div class="result-grid">
                <div class="result-card category-card">
                    <div class="card-icon">{category_icon}</div>
                    <div class="card-label">Kategori Keluhan</div>
                    <div class="card-value">{kategori}</div>
                </div>

                <div class="result-card priority-card">
                    <div class="card-icon">{priority_icon}</div>
                    <div class="card-label">Tingkat Prioritas</div>
                    <div class="card-value">{prioritas}</div>
                </div>

                <div class="result-card unit-card">
                    <div class="card-icon">🏢</div>
                    <div class="card-label">Unit Penanganan</div>
                    <div class="card-value">{unit}</div>
                </div>
            </div>

            <div class="summary-box">
                <strong>Keterangan prioritas:</strong><br>
                {priority_info}
                <br><br>
                <strong>Ringkasan:</strong><br>
                Keluhan tersebut masuk kategori <strong>{kategori}</strong>
                dengan prioritas <strong>{prioritas}</strong>.
                Sistem merekomendasikan laporan diteruskan ke
                <strong>{unit}</strong>.
            </div>
        </div>
        """
    )


def render_flow():
    render_html(
        """
        <div class="flow-grid">
            <div class="flow-card">
                <div class="flow-icon">💬</div>
                <div class="flow-title">Input Keluhan</div>
                <div class="flow-desc">
                    Mahasiswa menuliskan keluhan melalui kolom input aplikasi.
                </div>
            </div>

            <div class="flow-card">
                <div class="flow-icon">🧹</div>
                <div class="flow-title">Preprocessing</div>
                <div class="flow-desc">
                    Sistem membersihkan teks agar siap diproses oleh model.
                </div>
            </div>

            <div class="flow-card">
                <div class="flow-icon">🤖</div>
                <div class="flow-title">Prediksi Model</div>
                <div class="flow-desc">
                    Model memprediksi kategori dan tingkat prioritas keluhan.
                </div>
            </div>

            <div class="flow-card">
                <div class="flow-icon">🏢</div>
                <div class="flow-title">Unit Penanganan</div>
                <div class="flow-desc">
                    Sistem menampilkan rekomendasi unit layanan kampus.
                </div>
            </div>
        </div>
        """
    )


def render_unit_mapping():
    render_html(
        """
        <div class="soft-card">
            <div class="section-title">Rekomendasi Unit Penanganan</div>
            <div class="unit-grid">
                <div class="unit-item">
                    <span class="unit-category">📚 Akademik</span>
                    <span class="unit-target">Program Studi / Jurusan</span>
                </div>
                <div class="unit-item">
                    <span class="unit-category">📄 Administrasi</span>
                    <span class="unit-target">BAAK / Administrasi Fakultas</span>
                </div>
                <div class="unit-item">
                    <span class="unit-category">💳 Keuangan</span>
                    <span class="unit-target">BPPK / Bagian Keuangan</span>
                </div>
                <div class="unit-item">
                    <span class="unit-category">📡 Jaringan</span>
                    <span class="unit-target">UPT TIK / Tim Jaringan</span>
                </div>
                <div class="unit-item">
                    <span class="unit-category">🏫 Fasilitas</span>
                    <span class="unit-target">Sarana dan Prasarana</span>
                </div>
                <div class="unit-item">
                    <span class="unit-category">🧹 Kebersihan</span>
                    <span class="unit-target">Sarana dan Prasarana</span>
                </div>
                <div class="unit-item">
                    <span class="unit-category">🛡️ Keamanan</span>
                    <span class="unit-target">Satpam / Unit Keamanan Kampus</span>
                </div>
            </div>
        </div>
        """
    )


def render_about():
    render_html(
        """
        <div class="soft-card">
            <div class="about-grid">
                <div class="about-text">
                    <strong>E-Complaint Smart Campus</strong> merupakan aplikasi
                    untuk membantu pengelolaan keluhan mahasiswa secara lebih terarah.
                    Sistem ini memanfaatkan Natural Language Processing dan model
                    Machine Learning untuk mengklasifikasikan keluhan, menentukan
                    tingkat prioritas, serta memberikan rekomendasi unit penanganan.
                    <br><br>

                    <strong>Peran Software Engineering</strong><br>
                    Bagian Software Engineering berfokus pada implementasi model ke dalam
                    aplikasi web, perancangan antarmuka, integrasi model, serta deployment
                    agar sistem dapat diakses secara online.
                </div>

                <div>
                    <div class="section-title">Kelompok 10</div>

                    <div class="member-card">
                        <div class="member-name">1. Zacky Fiqran Kasmada</div>
                        <div class="member-nim">F1G123038</div>
                    </div>

                    <div class="member-card">
                        <div class="member-name">2. Andi Nanis Sacharina</div>
                        <div class="member-nim">F1G123018</div>
                    </div>

                    <div class="member-card">
                        <div class="member-name">3. Riby Sesharia Ramba</div>
                        <div class="member-nim">F1G123013</div>
                    </div>

                    <div class="member-card">
                        <div class="member-name">4. Melani Cicelia Saputri Lapake</div>
                        <div class="member-nim">F1G124012</div>
                    </div>

                    <div class="member-card">
                        <div class="member-name">5. Alifah Lauthfiyah Nurwasilah</div>
                        <div class="member-nim">F1G124002</div>
                    </div>

                    <div class="member-card">
                        <div class="member-name">6. La Ode Alifatur Yakin</div>
                        <div class="member-nim">F1G124___</div>
                    </div>
                </div>
            </div>
        </div>
        """
    )


def render_footer():
    render_html(
        """
        <div class="footer">
            🎓 E-Complaint Smart Campus · Kelompok 10 · NLP dan Machine Learning
        </div>
        """
    )