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

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 tidak ditemukan!"
    echo ""
    echo "Install Python 3.10+:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "  CentOS/RHEL:   sudo yum install python3"
    echo "  Mac:            brew install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo "Python: $PYTHON_VERSION"

echo "[1/4] Membuat virtual environment..."
python3 -m venv venv

echo "[2/4] Mengaktifkan virtual environment..."
source venv/bin/activate

echo "[3/4] Menginstall dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[4/4] Membuat folder yang diperlukan..."
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
