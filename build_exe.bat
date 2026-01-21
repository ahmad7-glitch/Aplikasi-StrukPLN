@echo off
title Build EXE - Aplikasi Struk PLN
color 0B

echo ============================================
echo   BUILD EXECUTABLE (.EXE)
echo   Aplikasi Struk PLN Pascabayar
echo ============================================
echo.

REM Cek Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python tidak ditemukan!
    pause
    exit
)

REM Install PyInstaller jika belum ada
echo [1/3] Menginstall PyInstaller dan dependencies...
python -m pip install --upgrade pip
python -m pip install pyinstaller reportlab

echo.
echo [2/3] Membuat executable...
echo Proses ini membutuhkan waktu beberapa menit...
echo.

REM Build executable dengan python -m pyinstaller (menghindari masalah PATH)
python -m PyInstaller --onefile --windowed --name "StrukPLN" --icon=NONE pln_pascabayar_struk_final_tampilan_rapi.py

echo.
if exist "dist\StrukPLN.exe" (
    echo [3/3] BUILD BERHASIL!
    echo.
    echo File executable tersimpan di folder: dist\StrukPLN.exe
    echo.
    echo Anda dapat menyalin file StrukPLN.exe ke lokasi manapun
    echo dan menjalankannya tanpa Python.
    echo.
    echo CATATAN: File .exe ukurannya besar (20-40 MB) karena berisi Python runtime.
    echo.
    start dist
) else (
    echo ERROR: Build gagal!
    echo Periksa pesan error di atas.
)

echo.
pause