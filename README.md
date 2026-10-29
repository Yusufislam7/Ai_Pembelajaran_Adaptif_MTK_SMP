# AI Pembelajaran Adaptif SMP

Aplikasi pembelajaran matematika berbasis Streamlit yang menyesuaikan penyajian materi berdasarkan gaya belajar dan prediksi kemampuan siswa. Model prediksi menggunakan `DecisionTreeClassifier` dari scikit-learn yang dilatih dari data pada `data/siswa.csv`.

## Fitur

- Mengumpulkan nama, nilai pre-test, dan gaya belajar siswa.
- Memprediksi kategori kemampuan siswa: `sangat_rendah`, `rendah`, `sedang`, atau `tinggi`.
- Menampilkan materi dengan penekanan visual, verbal, atau aktivitas praktik sesuai gaya belajar.
- Menyajikan latihan bertahap dalam empat level dan mengevaluasi jawaban.
- Menambah atau mengurangi skor dan dapat mengarahkan siswa kembali ke level sebelumnya.
- Menyediakan visualisasi pohon keputusan melalui skrip terpisah.

## Teknologi

- Python
- Streamlit
- pandas
- scikit-learn
- matplotlib (untuk visualisasi pohon keputusan)

## Menjalankan aplikasi

Pastikan Python dan `pip` sudah terpasang. Dari direktori proyek, jalankan perintah berikut di PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install streamlit pandas scikit-learn matplotlib
streamlit run streamlit_app.py
```

Streamlit akan menampilkan alamat lokal aplikasi di terminal, biasanya `http://localhost:8501`.

Jika PowerShell tidak mengizinkan aktivasi environment, gunakan executable environment secara langsung:

```powershell
.\.venv\Scripts\python.exe -m pip install streamlit pandas scikit-learn matplotlib
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

## Visualisasi model

Untuk membuka diagram pohon keputusan yang dilatih dari data siswa:

```powershell
python visualisasi_tree.py
```

Skrip ini menampilkan visualisasi menggunakan matplotlib dan memerlukan lingkungan yang mendukung jendela grafik.

## Alur aplikasi

1. Siswa mengisi nama, nilai awal (0–100), dan gaya belajar.
2. `model_ai.py` memuat `data/siswa.csv`, mengubah nilai kategori menjadi angka dengan `LabelEncoder`, lalu melatih pohon keputusan dengan `max_depth=3`.
3. Prediksi kemampuan menggunakan nilai saat ini dan gaya belajar. Prediksi tersebut digunakan untuk memberi label profil dan menyesuaikan teks materi.
4. Siswa membaca materi level saat ini dan mengerjakan lima soal dari `soal.json`.
5. Jika sedikitnya empat jawaban benar, skor bertambah 20. Siswa naik level jika skor baru memenuhi ambang level tersebut.
6. Jika kurang dari empat jawaban benar, skor dikurangi 15 (minimum 0). Pada level di atas 1, siswa turun satu level jika skor berada di bawah ambang level sebelumnya.
7. Setelah melewati level terakhir, aplikasi menampilkan status bahwa seluruh materi telah selesai.

Ambang skor untuk melanjutkan level adalah:

| Level | Skor minimum |
|---|---:|
| 1 | 40 |
| 2 | 55 |
| 3 | 70 |
| 4 | 85 |

## Struktur proyek

```text
.
├── streamlit_app.py          # Antarmuka dan alur pembelajaran
├── model_ai.py               # Pelatihan dan prediksi kemampuan
├── visualisasi_tree.py       # Visualisasi pohon keputusan
├── soal.json                 # Soal dan kunci jawaban untuk tiap level
├── data/
│   └── siswa.csv             # Data contoh untuk melatih model
└── materi/
    ├── materi_level.json     # Materi, informasi visual, dan aktivitas per level
    └── materi_gaya.json      # Deskripsi gaya belajar
```

Data siswa dibaca dari CSV saat modul model dijalankan. `materi_gaya.json` tersedia dalam proyek, tetapi belum dibaca oleh aplikasi; adaptasi gaya belajar saat ini menggunakan kondisi yang ditulis langsung di `streamlit_app.py`.

## Catatan implementasi

- Model dilatih ulang dari CSV setiap kali modul model dimuat; tidak ada berkas model terlatih yang disimpan.
- Dataset berisi 20 baris contoh. Hasil prediksi merupakan demonstrasi prototipe dan belum cukup untuk menyimpulkan kemampuan siswa secara umum.
- Kolom `level_kognitif` pada CSV belum digunakan sebagai fitur maupun label model.
- Materi level 1 membahas operasi hitung bilangan bulat, sedangkan soal level 1 saat ini berisi persamaan dan operasi aljabar. Materi dan soal sebaiknya diselaraskan sebelum digunakan sebagai konten pembelajaran.
- Skor pada aplikasi merupakan skor kumulatif: nilai awal siswa dapat bertambah atau berkurang selama latihan.
- Sesi belajar disimpan sementara di Streamlit session state dan tidak dicatat sebagai riwayat permanen.
