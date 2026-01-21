@echo off
title Install Dependencies - Aplikasi Struk PLN
color 0E

echo ============================================
echo   INSTALL DEPENDENCIES
echo   Aplikasi Struk PLN Pascabayar
echo ============================================
echo.

REM Cek Python
python --version
if errorlevel 1 (
    echo.
    echo ERROR: Python tidak ditemukan!
    echo Silakan install Python dari: https://www.python.org/downloads/
    echo.
    pause
    exit
)

echo.
echo Menginstall package yang dibutuhkan...
echo.

REM Upgrade pip
python -m pip install --upgrade pip

REM Install reportlab untuk PDF
pip install reportlab

echo.
echo ============================================
echo   INSTALASI SELESAI!
echo ============================================
echo.
echo Dependencies yang terinstall:
echo - reportlab (untuk export PDF)
echo - tkinter (sudah include di Python)
echo.
echo Anda sekarang dapat menjalankan aplikasi dengan:
echo 1. Double-click file: run_struk_pln.bat
echo 2. Atau jalankan: python pln_pascabayar_struk_final_tampilan_rapi.py
echo.
pause