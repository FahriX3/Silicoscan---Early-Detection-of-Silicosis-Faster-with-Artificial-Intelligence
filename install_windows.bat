@echo off
REM ================================================
REM Silicoscan — Windows Installer
REM ================================================
REM Sistem Skrining Paru-Paru AI untuk Silikosis
REM ================================================

echo.
echo ================================================
echo   Silicoscan - Installer Windows
echo   Skrining Paru-Paru AI untuk Silikosis
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo.
    echo Silakan install Python 3.10+ dari:
    echo   https://www.python.org/downloads/
    echo.
    echo PENTING: Centang "Add Python to PATH" saat instalasi!
    echo.
    pause
    exit /b 1
)

echo [1/4] Membuat virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Gagal membuat virtual environment
    pause
    exit /b 1
)

echo [2/4] Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Menginstall dependencies (ini bisa memakan waktu beberapa menit)...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Gagal install dependencies
    pause
    exit /b 1
)

echo [4/4] Membuat folder yang diperlukan...
if not exist "uploads" mkdir uploads
if not exist "results" mkdir results
if not exist "models" mkdir models

echo.
echo ================================================
echo   Instalasi Selesai!
echo ================================================
echo.
echo   Cara menjalankan:
echo     1. Buka Command Prompt di folder ini
echo     2. Jalankan: run.bat
echo.
echo   Atau manual:
echo     venv\Scripts\activate
echo     python app.py
echo.
echo   Lalu buka browser: http://localhost:8000
echo ================================================
echo.
pause
