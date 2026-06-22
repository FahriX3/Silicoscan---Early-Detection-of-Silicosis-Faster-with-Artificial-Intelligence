#!/bin/bash
# ================================================
# Silicoscan — Linux/Mac Installer
# ================================================
# Sistem Skrining Paru-Paru AI untuk Silikosis
# ================================================

set -e

echo ""
echo "================================================"
echo "  Silicoscan - Installer Linux/Mac"
echo "  Skrining Paru-Paru AI untuk Silikosis"
echo "================================================"
echo ""

echo "[1/5] Memeriksa dependensi sistem operasi..."
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    echo "  -> Python3/pip tidak ditemukan. Mencoba menginstal otomatis..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install python3 python3-venv python3-pip libgl1-mesa-glx libglib2.0-0 -y
    elif command -v yum &> /dev/null; then
        sudo yum install python3 python3-pip mesa-libGL -y
    elif command -v brew &> /dev/null; then
        brew install python3
    else
        echo "[ERROR] Sistem operasi tidak didukung untuk instalasi otomatis."
        echo "Silakan install Python 3.10+ secara manual."
        exit 1
    fi
else
    echo "  -> Python3 sudah terinstall."
    # Coba install libgl1 khusus untuk ubuntu jika apt tersedia (supaya OpenCV tidak error)
    if command -v apt-get &> /dev/null; then
        sudo apt-get install libgl1-mesa-glx libglib2.0-0 -y > /dev/null 2>&1 || true
    fi
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo "Python: $PYTHON_VERSION"

echo "[2/5] Membuat virtual environment..."
python3 -m venv venv

echo "[3/5] Mengaktifkan virtual environment..."
source venv/bin/activate

echo "[4/5] Menginstall dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[5/5] Membuat folder yang diperlukan..."
mkdir -p uploads results models

echo ""
echo "================================================"
echo "  Instalasi Selesai!"
echo "================================================"
echo ""
echo "  Cara menjalankan:"
echo "    source venv/bin/activate"
echo "    python app.py"
echo ""
echo "  Atau gunakan:"
echo "    chmod +x run.sh"
echo "    ./run.sh"
echo ""
echo "  Lalu buka browser: http://localhost:8000"
echo "================================================"
echo ""
