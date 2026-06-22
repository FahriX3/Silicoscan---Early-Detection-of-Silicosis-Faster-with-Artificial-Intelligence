# <img src="static/img/logo.png" height="32" align="center" alt="logo"> Silicoscan

**Sistem Skrining Paru-Paru Berbasis AI untuk Deteksi Dini Silikosis**

Aplikasi web prototipe untuk skrining awal kondisi paru-paru pekerja tambang menggunakan foto rontgen dada (chest X-ray). Sistem ini dirancang ringan dan portabel (Portable Edition) dengan menggunakan format ONNX, yang menjalankan pipeline dua tahap untuk memberikan hasil analisis yang komprehensif.

---

## 🔬 Arsitektur & Cara Kerja

Sistem ini tidak lagi menggunakan classifier terpisah, melainkan langsung berfokus pada melokalisasi dan mendeteksi probabilitas abnormalitas menggunakan pendekatan deteksi objek setelah paru-paru disegmentasi.

```text
Upload X-Ray → [U-Net Masking] → [YOLO Detection] → Hasil Lokasi & Kelas Abnormalitas 🔍
```

### 2 Tahap Pipeline AI:

| Tahap | Model AI | Format & Kompresi | Fungsi Utama |
|-------|-----------|--------|--------------|
| **Tahap 1: Segmentasi Paru** | U-Net (ResNet34 backbone) | ONNX (FP32) | Memotong (crop) area paru-paru dari *background* untuk menghilangkan noise di luar region-of-interest. |
| **Tahap 2: Deteksi Lesi** | YOLO11s | ONNX (FP16) | Mencari, mendeteksi, dan menandai lokasi spesifik serta memberikan nilai *confidence* untuk setiap temuan. |

### Pilihan Model Deteksi
Terdapat 2 opsi model deteksi yang dapat dipilih pengguna saat melakukan skrining:
1. **Model Deteksi Biasa (3 Kelompok Utama)**: Mengelompokkan penyakit paru menjadi 3 kategori: *Silicosis Nodular*, *Silicosis Advanced Fibrotic*, dan *Other Lung Abnormality*.
2. **Model Deteksi Full (11 Kelas Detail)**: Mendeteksi kelainan secara spesifik dari 11 kelas tanpa pengelompokan.

---

## 🎯 Tingkat Akurasi
Model-model AI pada aplikasi ini telah melalui proses *training* dan validasi pada dataset citra rontgen pekerja tambang. Optimalisasi kompresi ke format ONNX (*FP16* untuk deteksi, *FP32* untuk masking) menjaga tingkat akurasi tetap presisi dengan konsumsi *resource* hardware yang jauh lebih efisien dan ringan.

---

## 🚀 Cara Pakai & Instalasi (Portable)

Aplikasi ini sudah dioptimalkan agar sepenuhnya **mandiri (standalone)**. Seluruh model dan *dependencies* sudah dirancang agar dapat langsung dijalankan di sistem operasi standar tanpa perlu pengaturan Python PyTorch yang berat.

### 🪟 Windows

Seluruh proses pembuatan *Virtual Environment* dan pengunduhan *library* akan dilakukan secara otomatis.
**Prasyarat**: Pastikan [Python 3.10+](https://www.python.org/downloads/) sudah terinstall (Centang "Add Python to PATH" saat instalasi).

1. Buka folder `Web Interface` di File Explorer.
2. Klik ganda pada file `install_windows.bat` (Hanya perlu dilakukan 1x di awal).
3. Untuk menjalankan aplikasi, klik ganda pada `run.bat`.

### 🍏 Linux / macOS (Otomatis Penuh)

Script instalasi Linux/macOS sudah dilengkapi sistem pendeteksi OS. Jika Python atau *library* grafis OS belum ada, script akan **otomatis mengunduhkannya** via `apt-get` (Ubuntu/Debian), `yum` (CentOS/RHEL), atau `brew` (Mac).

Buka Terminal di dalam folder `Web Interface` lalu jalankan:
1. **Beri izin eksekusi**:
   ```bash
   chmod +x install_linux.sh run.sh
   ```
2. **Jalankan Installer** (Mungkin akan meminta password `sudo` untuk install dependencies OS):
   ```bash
   ./install_linux.sh
   ```
3. **Menjalankan Server**:
   ```bash
   ./run.sh
   ```

### 🐳 Menggunakan Docker (Rekomendasi Terbaik)

Jika tidak mau pusing memikirkan Python versi berapa dan OS apa, gunakan Docker. Folder `Web Interface` ini sudah **100% Standalone**, tidak membutuhkan folder lain di luarnya.

```bash
docker-compose up -d
```
Aplikasi akan langsung berjalan secara *containerized* di *background*. Cocok untuk rilis produksi di server VPS.

---

## 🌐 Cara Penggunaan (Web Interface)

1. Buka browser dan akses: **http://localhost:8000**
2. Pilih opsi **Mulai Skrining**.
3. Unggah foto rontgen dada dengan format standar (JPG/PNG/JPEG).
4. Pilih **Model Deteksi** (Biasa atau Full) dari menu *dropdown*.
5. Klik **Mulai Analisis AI**.
6. Sistem akan mengeksekusi pipeline dan menampilkan gambar hasil segmentasi dan hasil *bounding box* lesi dalam hitungan detik (kurang dari 5 detik).

---

## ⚙️ Konfigurasi Lanjutan
Untuk kebutuhan riset atau *tweaking*, modifikasi file `config.py` untuk menyesuaikan:
- *Confidence threshold* deteksi AI
- Path atau letak model ONNX 
- Warna *bounding box* untuk setiap kelas penyakit

---

## 🛠️ Tech Stack & Modul

- **Backend / API**: FastAPI + Uvicorn
- **AI Inference Engine**: ONNX Runtime (Super ringan & CPU-friendly)
- **Image Processing**: OpenCV, NumPy, Pillow
- **Frontend**: Vanilla HTML / CSS (Flexbox & CSS Grid) / JS (Asynchronous Fetch)

---

## ⚠️ Disclaimer Medis

Aplikasi ini dikembangkan untuk keperluan prototipe dan riset keselamatan kesehatan kerja (K3) untuk deteksi awal *Silikosis*. Hasil yang diberikan **BUKAN** merupakan diagnosis medis akhir. Selalu lakukan validasi dan pemeriksaan klinis bersama ahli medis (Radiolog/Dokter Paru) yang berwenang.
