@echo off
title Aplikasi Struk PLN Pascabayar
color 0A

echo ============================================
echo   APLIKASI STRUK PLN PASCABAYAR
echo ============================================
echo.
echo Memulai aplikasi...
echo.

REM Cek apakah Python terinstall
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python tidak ditemukan!
    echo Silakan install Python terlebih dahulu dari https://www.python.org
    pause
    exit
)

REM Cek dan install dependencies
echo Memeriksa dependencies...
pip install reportlab >nul 2>&1

REM Jalankan aplikasi
python pln_pascabayar_struk_final_tampilan_rapi.py

if errorlevel 1 (
    echo.
    echo ERROR: Aplikasi gagal dijalankan!
    echo Pastikan file pln_pascabayar_struk_final_tampilan_rapi.py ada di folder ini.
    pause
)