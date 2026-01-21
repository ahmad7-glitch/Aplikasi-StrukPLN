# 📋 Aplikasi Struk PLN Pascabayar

Aplikasi desktop untuk membuat dan mencetak struk pembayaran tagihan listrik PLN Pascabayar dengan tampilan modern dan profesional.

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## ✨ Fitur Unggulan

- 🔍 **Pencarian Cerdas** - Dropdown autocomplete untuk mencari pelanggan
- 🧮 **Kalkulasi Otomatis** - Total pembayaran dihitung secara otomatis
- 👁️ **Preview Print** - Lihat struk sebelum mencetak
- 💾 **Export PDF** - Simpan struk sebagai PDF dengan nama otomatis (ID_Pelanggan_Tanggal)
- 🖨️ **Print Langsung** - Cetak langsung ke printer thermal atau biasa
- 💎 **UI Modern** - Tampilan profesional dengan color scheme yang menarik
- 📊 **87 Data Pelanggan** - Database pelanggan siap pakai
- 📱 **Responsive** - Layout fleksibel yang bisa diresize

## 🚀 Cara Menjalankan

### Metode 1: Quick Start (Termudah) ⚡
1. **Install Dependencies** (Hanya sekali)
   - Double-click: `install_dependencies.bat`
   - Tunggu sampai selesai

2. **Jalankan Aplikasi**
   - Double-click: `run_struk_pln.bat`
   - Aplikasi akan otomatis terbuka

### Metode 2: Manual dengan Python 🐍
```bash
# Install dependencies
pip install reportlab

# Jalankan aplikasi
python pln_pascabayar_struk_final_tampilan_rapi.py
```

## 📦 Membuat File EXE (Portable)

### Cara Otomatis (Recommended) 🎯
1. Double-click: `build_exe.bat`
2. Tunggu proses build (2-3 menit)
3. File `StrukPLN.exe` akan ada di folder `dist/`
4. Copy file `.exe` ke komputer manapun tanpa perlu Python!

### Cara Manual 🔧
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "StrukPLN" pln_pascabayar_struk_final_tampilan_rapi.py

# File .exe ada di folder: dist/StrukPLN.exe
```

## 📋 Requirements

### Minimum
- **OS**: Windows 7/8/10/11, Linux, macOS
- **Python**: 3.7 atau lebih baru
- **RAM**: 256 MB
- **Storage**: 50 MB

### Dependencies
- `tkinter` - GUI framework (included in Python)
- `reportlab` - PDF generation library

Install dengan:
```bash
pip install reportlab
```

## 💻 Struktur Folder

```
Aplikasi-StrukPLN/
│
├── pln_pascabayar_struk_final_tampilan_rapi.py   # File utama aplikasi
├── run_struk_pln.bat                              # Launcher aplikasi
├── build_exe.bat                                  # Builder untuk .exe
├── install_dependencies.bat                       # Installer dependencies
├── README.md                                      # Dokumentasi
├── requirements.txt                               # List dependencies
└── LICENSE                                        # Lisensi MIT
```

## 📖 Panduan Penggunaan

### 1️⃣ Input Data Pelanggan
- Pilih **ID Pelanggan** atau **Nama** dari dropdown
- Ketik untuk mencari pelanggan
- Data akan otomatis terisi

### 2️⃣ Input Detail Tagihan
- **Tarif/Daya**: Masukkan tarif dan daya listrik
- **Tagihan PLN**: Masukkan nominal tagihan
- **Admin Bank**: Masukkan biaya admin
- **Total Bayar**: Otomatis terhitung

### 3️⃣ Generate & Simpan
- Klik **📄 Generate Struk** untuk melihat preview
- Klik **💾 Simpan PDF** untuk export ke file PDF
- Klik **🖨️ Print** untuk preview dan cetak ke printer

## 🎨 Screenshot

### Tampilan Utama
![Main Interface](https://i.ibb.co.com/CKFcY1c6/Tampilan-awal-Struk-PLN.png)

### Preview Print
![Print Preview](https://i.ibb.co.com/jnNFrGS/Tampilan-Print-Preview-Struk-PLN.png)

## 🔧 Troubleshooting

### Aplikasi tidak bisa dibuka?
**Solusi:**
1. Pastikan Python sudah terinstall
2. Jalankan: `install_dependencies.bat`
3. Atau manual: `pip install reportlab`

### Error saat build EXE?
**Solusi:**
1. Pastikan PyInstaller terinstall: `pip install pyinstaller`
2. Hapus folder `build` dan `dist`
3. Jalankan ulang `build_exe.bat`

### PDF tidak bisa dibuat?
**Solusi:**
1. Install reportlab: `pip install reportlab`
2. Restart aplikasi

### Font emoji tidak muncul?
**Solusi:**
- Di Windows: Update ke Windows 10/11
- Di Linux: Install `fonts-noto-color-emoji`

### Print tidak berfungsi?
**Solusi:**
1. Pastikan printer sudah terinstall
2. Set printer sebagai default printer
3. Cek koneksi printer

## 🎯 Tips & Tricks

1. **Shortcut Keyboard**
   - Gunakan Tab untuk navigasi antar field
   - Enter untuk submit form

2. **Format Angka**
   - Tagihan: Bisa input dengan/tanpa titik
   - Otomatis: 100000 atau 100.000

3. **Nama File PDF**
   - Format: `{ID_PELANGGAN}_{YYYYMMDD_HHMMSS}.pdf`
   - Contoh: `533310631413_20240115_143052.pdf`

4. **Backup Data**
   - Simpan folder `Aplikasi-StrukPLN` secara berkala
   - Database pelanggan ada di kode Python

## 🔄 Update & Maintenance

### Menambah Data Pelanggan
Edit file `pln_pascabayar_struk_final_tampilan_rapi.py`:

```python
DATA_PELANGGAN = [
    ("ID_BARU", "NAMA_PELANGGAN"),
    # ... existing data ...
]
```

### Update UI Theme
Edit variabel warna di bagian:
```python
BG_COLOR = "#f0f4f8"
PRIMARY_COLOR = "#2563eb"
# ... etc ...
```

## 📄 License

MIT License - Bebas digunakan dan dimodifikasi untuk keperluan apapun.

## 👨‍💻 Developer

Dikembangkan dengan ❤️ untuk memudahkan proses administrasi pembayaran PLN.

## 📞 Support

Untuk bantuan, saran, atau laporan bug:
- 📧 Email: support@contoh.com
- 💬 Issue: [GitHub Issues](https://github.com/username/repo/issues)

## 🌟 Fitur Mendatang (Roadmap)

- [ ] Database eksternal (SQLite)
- [ ] Laporan bulanan
- [ ] Multi-user dengan login
- [ ] History transaksi
- [ ] Export ke Excel
- [ ] Notifikasi pembayaran
- [ ] Integrasi API PLN (jika tersedia)

## 📝 Changelog

### Version 1.0 (2024-01-15)
- ✅ Initial release
- ✅ UI modern dengan Tkinter
- ✅ 87 data pelanggan
- ✅ Export PDF
- ✅ Print support
- ✅ Auto calculation
- ✅ Search & autocomplete

---

**Made with ❤️ by [Ahmad Digital]**

*Last Updated: January 2026*
