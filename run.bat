@echo off
REM ================================================
REM Silicoscan — Run Script (Windows)
REM ================================================

echo.
echo   Silicoscan - Starting...
echo.

call venv\Scripts\activate.bat
python app.py

pause
