@echo off
title Build EXE - Aplikasi Struk PLN (Simple)
color 0B

echo ============================================
echo   BUILD EXECUTABLE (.EXE) - SIMPLE VERSION
echo   Aplikasi Struk PLN Pascabayar
echo ============================================
echo.

REM Pastikan PyInstaller terinstall
echo Installing PyInstaller...
python -m pip install --upgrade pip
python -m pip install pyinstaller reportlab
echo.

REM Build dengan opsi minimal
echo Building executable...
python -m PyInstaller --onefile --windowed ^
    --name "StrukPLN" ^
    --add-data "*.py;." ^
    pln_pascabayar_struk_final_tampilan_rapi.py

echo.
if exist "dist\StrukPLN.exe" (
    echo ============================================
    echo   BUILD BERHASIL!
    echo ============================================
    echo.
    echo File: dist\StrukPLN.exe
    echo Ukuran: ~30-40 MB (termasuk Python runtime)
    echo.
    echo Membuka folder dist...
    start dist
    echo.
    echo SELESAI!
) else (
    echo ============================================
    echo   BUILD GAGAL!
    echo ============================================
    echo.
    echo Silakan jalankan manual dengan command:
    echo python -m PyInstaller --onefile --windowed --name "StrukPLN" pln_pascabayar_struk_final_tampilan_rapi.py
)

echo.
pause