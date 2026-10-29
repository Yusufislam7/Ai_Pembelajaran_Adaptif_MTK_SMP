import streamlit as st
import json
from model_ai import prediksi_kemampuan

# ================= 1. LOAD DATA =================
with open("materi/materi_level.json", "r", encoding="utf-8") as f:
    materi_level = json.load(f)

with open("soal.json", "r", encoding="utf-8") as f:
    soal_data = json.load(f)

# ================= 2. KONFIGURASI =================
SYARAT_NILAI = {
    1: 40,
    2: 55,
    3: 70,
    4: 85
}

MAX_LEVEL = max(int(k) for k in soal_data.keys())

# ================= 3. AI CONTENT TRANSFORMER (POIN 4) =================
def update_materi_dengan_ai(materi_obj, gaya, kemampuan):
    """
    Fungsi ini memenuhi Poin 4: Hasil klasifikasi AI memodifikasi 
    konten secara dinamis berdasarkan gaya belajar dan kemampuan.
    """
    materi_raw = materi_obj["materi"]
    visual = materi_obj["visual_info"]
    praktik = materi_obj["aktivitas"]
    objek = materi_obj["objek"]

    prefix = f"### 🤖 Rekomendasi Materi: {objek} (Profil: {kemampuan.upper()})\n"
    
    # AI Memilih dan Menyusun Konten Berdasarkan Klasifikasi Gaya Belajar
    if gaya == "visual":
        konten_utama = f"**[Fokus Visualisasi]**\n{materi_raw}\n\n**🔍 Instruksi Visual AI:** {visual}"
    elif gaya == "kinestetik":
        konten_utama = f"**[Fokus Aktivitas Praktik]**\n{materi_raw}\n\n**🛠️ Instruksi Interaktif AI:** {praktik}"
    else: # verbal
        konten_utama = f"**[Fokus Narasi Konseptual]**\n{materi_raw}\n\n*Instruksi AI: Bacalah langkah-langkah logis di atas secara sistematis.*"
    
    # Penyesuaian Konten Berdasarkan Klasifikasi Kemampuan (Literasi)
    catatan = ""
    if kemampuan in ["sangat_rendah", "rendah"]:
        catatan = "\n\n⚠️ **Catatan AI:** Materi telah disederhanakan untuk memperkuat literasi dasar Anda."

    return prefix + konten_utama + catatan

# ================= 4. SETTING PAGE =================
st.set_page_config(page_title="AI Pembelajaran Adaptif", layout="centered")
st.title("🤖 AI Pembelajaran Adaptif SMP")
st.markdown("#### Topik: Literasi Matematis berbasis Pembelajaran Adaptif")

# ================= 5. SESSION STATE =================
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.level = 1
    st.session_state.nilai = 0
    st.session_state.jawaban = {}

# ================= 6. HALAMAN INPUT (PRE-TEST) =================
if not st.session_state.started:
    st.sidebar.info("Gunakan Pre-test untuk identifikasi awal oleh Decision Tree AI.")
    nama = st.text_input("Nama Siswa", placeholder="Masukkan nama Anda...")
    nilai_awal = st.slider("Nilai Pre-test (Feedback Awal)", 0, 100, 20)
    gaya = st.selectbox("Gaya Belajar", ["visual", "verbal", "kinestetik"])

    if st.button("🚀 Mulai Pembelajaran"):
        if nama:
            st.session_state.nama = nama
            st.session_state.nilai = nilai_awal
            st.session_state.gaya = gaya
            st.session_state.started = True
            st.rerun()
        else:
            st.warning("Silakan masukkan nama terlebih dahulu.")

# ================= 7. HALAMAN UTAMA PEMBELAJARAN =================
else:
    nama = st.session_state.nama
    nilai = st.session_state.nilai
    level = st.session_state.level

    # Check Goal State
    if level > MAX_LEVEL:
        st.balloons()
        st.success(f"🏁 GOAL STATE TERCAPAI! Selamat {nama}!")
        st.write("Anda telah menguasai seluruh materi literasi matematis level SMP.")
        if st.button("Ulangi dari Awal"):
            st.session_state.clear()
            st.rerun()
        st.stop()

    # (3) Identifikasi/Klasifikasi Feedback Menggunakan Model AI
    kemampuan = prediksi_kemampuan(nilai, st.session_state.gaya)

    # (4) UPDATE MATERI MENGGUNAKAN AI BERDASARKAN FEEDBACK
    # Mengambil objek materi lengkap dari database JSON
    objek_materi_lengkap = materi_level[str(level)]
    materi_adaptif = update_materi_dengan_ai(objek_materi_lengkap, st.session_state.gaya, kemampuan)

    # ===== HEADER PROFIL =====
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"👤 **Siswa:** {nama}")
        st.write(f"📈 **Level Saat Ini:** {level}")
    with col2:
        st.write(f"🎯 **Prediksi Kemampuan:** {kemampuan}")
        st.write(f"⭐ **Skor Literasi:** {nilai}")

    # (1) Siswa melihat materi (Content Adaptive)
    st.markdown("---")
    st.info(materi_adaptif)

    # ===== (2) SOAL LATIHAN (Mencari Feedback Pemahaman) =====
    st.markdown(f"### 📝 Latihan Level {level}")
    st.write("Selesaikan kuis di bawah ini untuk lanjut ke materi berikutnya:")
    
    for i, soal in enumerate(soal_data[str(level)], start=1):
        st.markdown(f"**Soal {i}:** {soal['pertanyaan']}")
        st.session_state.jawaban[i] = st.radio(
            "Pilih jawaban:", soal["opsi"], key=f"q{i}_{level}"
        )

   # ===== (5) EVALUASI & LOOPING =====
    if st.button("📝 Evaluasi Jawaban"):
        benar = 0
        total = len(soal_data[str(level)])
        nilai_min = SYARAT_NILAI[level]

        for i, soal in enumerate(soal_data[str(level)], start=1):
            if st.session_state.jawaban[i].startswith(soal["jawaban"]):
                benar += 1

        st.markdown(f"**Hasil Evaluasi: {benar}/{total} Benar**")

        if benar >= 4:
            st.session_state.nilai += 20 
            if st.session_state.nilai >= nilai_min:
                st.success(f"🎉 Hebat! Anda lulus Level {level}.")
                st.session_state.level += 1
                st.rerun()
            else:
                st.warning("⚠️ Jawaban benar, tapi skor akumulatif belum cukup.")
        else:
            # --- LOGIKA TURUN LEVEL (BACKWARD ADAPTATION) ---
            st.error("❌ Belum Lulus.")
            st.session_state.nilai = max(0, st.session_state.nilai - 15) # Penalti lebih besar jika salah banyak
            
            # Jika nilai drop di bawah ambang batas level sebelumnya, turunkan level
            if level > 1 and st.session_state.nilai < SYARAT_NILAI.get(level-1, 0):
                st.warning(f"🔄 AI mendeteksi kesulitan yang signifikan. Mengarahkan kembali ke Level {level-1} untuk penguatan dasar.")
                st.session_state.level -= 1
                st.rerun()