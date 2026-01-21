from tkinter import Tk, Frame, Label, Entry, Text, Button, filedialog, messagebox, font, Toplevel, Scrollbar, Canvas
from tkinter import ttk
from datetime import datetime
import tempfile
import os
import platform

# Cek apakah reportlab tersedia
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: reportlab tidak tersedia. Fitur PDF dinonaktifkan.")
    print("Install dengan: pip install reportlab")

# Data pelanggan dari rekap tagihan
DATA_PELANGGAN = [
    ("512345678910", "NAMA PELANGGAN 01"),
    ("512345678910", "NAMA PELANGGAN 02"),
]

# Data Tarif dan Daya PLN
DATA_TARIF_DAYA = [
    ("R-1", "450 VA"),
    ("R-1", "900 VA"),
    ("R-1", "1.300 VA"),
    ("R-1", "2.200 VA"),
    ("R-2", "3.500 VA"),
    ("R-2", "5.500 VA"),
    ("R-3", "6.600 VA"),
]

def cari_pelanggan(event=None):
    """Filter data pelanggan berdasarkan pencarian"""
    query = combo_idpel.get().lower()
    if not query:
        combo_idpel['values'] = [f"{idpel} - {nama}" for idpel, nama in DATA_PELANGGAN]
    else:
        filtered = [f"{idpel} - {nama}" for idpel, nama in DATA_PELANGGAN 
                   if query in idpel.lower() or query in nama.lower()]
        combo_idpel['values'] = filtered

def pilih_pelanggan(event=None):
    """Otomatis isi nama saat pelanggan dipilih"""
    selected = combo_idpel.get()
    if " - " in selected:
        idpel, nama = selected.split(" - ", 1)
        combo_idpel.delete(0, "end")
        combo_idpel.insert(0, idpel)
        combo_nama.delete(0, "end")
        combo_nama.insert(0, nama)

def cari_nama(event=None):
    """Filter data pelanggan berdasarkan pencarian nama"""
    query = combo_nama.get().lower()
    if not query:
        combo_nama['values'] = [f"{nama} - {idpel}" for idpel, nama in DATA_PELANGGAN]
    else:
        filtered = [f"{nama} - {idpel}" for idpel, nama in DATA_PELANGGAN 
                   if query in nama.lower() or query in idpel.lower()]
        combo_nama['values'] = filtered

def pilih_nama(event=None):
    """Otomatis isi IDPEL saat nama dipilih"""
    selected = combo_nama.get()
    if " - " in selected:
        nama, idpel = selected.split(" - ", 1)
        combo_nama.delete(0, "end")
        combo_nama.insert(0, nama)
        combo_idpel.delete(0, "end")
        combo_idpel.insert(0, idpel)

def hitung_total(event=None):
    """Hitung total bayar otomatis dari tagihan + admin"""
    try:
        tagihan_str = entry_tagihan.get().replace(".", "").replace(",", "").replace("Rp", "").strip()
        admin_str = entry_admin.get().replace(".", "").replace(",", "").replace("Rp", "").strip()
        
        tagihan = int(tagihan_str) if tagihan_str else 0
        admin = int(admin_str) if admin_str else 0
        
        total = tagihan + admin
        
        entry_total.config(state="normal")
        entry_total.delete(0, "end")
        if total > 0:
            entry_total.insert(0, f"{total:,}".replace(",", "."))
        entry_total.config(state="readonly")
    except ValueError:
        entry_total.config(state="normal")
        entry_total.delete(0, "end")
        entry_total.config(state="readonly")

def pilih_tarif_daya(event=None):
    """Otomatis isi tarif dan daya saat dipilih"""
    selected = combo_tarif_daya.get()
    if " - " in selected:
        tarif, daya = selected.split(" - ")
        combo_tarif_daya.delete(0, "end")
        combo_tarif_daya.insert(0, f"{tarif}/{daya}")

def cetak_struk():
    # Ambil tarif dan daya dari combo_tarif_daya
    tarif_daya = combo_tarif_daya.get()
    if not tarif_daya or tarif_daya == "Pilih Tarif & Daya":
        tarif_daya = "N/A"
    
    # Format struk sesuai contoh gambar BTN - dengan tag untuk bold
    struk_lines = []
    
    # Header
    struk_lines.append(("normal", "PT Bank Tabungan Negara (Persero) Tbk."))
    struk_lines.append(("normal", " " * 70 + "COPY"))
    struk_lines.append(("title", "            STRUK PEMBAYARAN TAGIHAN LISTRIK"))
    struk_lines.append(("normal", ""))
    
    # Data pelanggan
    struk_lines.append(("normal", f"IDPEL        : {combo_idpel.get():<30}BL/TH         : {entry_bulan.get()}"))
    struk_lines.append(("normal", f"NAMA         : {combo_nama.get():<30}STAND METER   : {entry_meter.get()}"))
    struk_lines.append(("normal", f"TARIF/DAYA   : {tarif_daya}"))
    struk_lines.append(("normal", f"RP TAG PLN   : RP           {entry_tagihan.get():<15}"))
    struk_lines.append(("bold", f"NO REF       : {entry_ref.get()}"))
    struk_lines.append(("normal", ""))
    
    # Pernyataan PLN
    struk_lines.append(("bold", "      PLN menyatakan struk ini sebagai bukti pembayaran yang sah."))
    struk_lines.append(("normal", ""))
    
    # Total pembayaran
    struk_lines.append(("normal", f"ADMIN BANK   : RP           {entry_admin.get():<15}"))
    struk_lines.append(("bold", f"TOTAL BAYAR  : RP           {entry_total.get():<15}"))
    struk_lines.append(("normal", ""))
    
    # Footer tengah
    struk_lines.append(("normal", " " * 34 + "Terima Kasih"))
    struk_lines.append(("normal", " " * 35 + "BANK BTN"))
    struk_lines.append(("normal", "     Informasi Hubungi Call Center 123 Atau Hub PLN Terdekat"))
    
    # Clear text widget
    text_struk.delete("1.0", "end")
    
    # Configure tags untuk bold dan title
    text_struk.tag_configure("bold", font=("Courier New", 10, "bold"))
    text_struk.tag_configure("title", font=("Courier New", 14, "bold"))
    text_struk.tag_configure("normal", font=("Courier New", 10))
    
    # Insert dengan formatting
    for tag, line in struk_lines:
        text_struk.insert("end", line + "\n", tag)

def simpan_struk():
    # Ambil tarif dan daya dari combo_tarif_daya
    tarif_daya = combo_tarif_daya.get()
    if not tarif_daya or tarif_daya == "Pilih Tarif & Daya":
        tarif_daya = "N/A"
    
    # Generate struk text (sama seperti cetak_struk tapi tanpa tags)
    struk_text = "PT Bank Tabungan Negara (Persero) Tbk." + " " * 31 + "COPY\n"
    struk_text += "            STRUK PEMBAYARAN TAGIHAN LISTRIK\n\n"
    
    struk_text += f"IDPEL        : {combo_idpel.get():<30}BL/TH         : {entry_bulan.get()}\n"
    struk_text += f"NAMA         : {combo_nama.get():<30}STAND METER   : {entry_meter.get()}\n"
    struk_text += f"TARIF/DAYA   : {tarif_daya}\n"
    struk_text += f"RP TAG PLN   : RP           {entry_tagihan.get():<15}\n"
    struk_text += f"NO REF       : {entry_ref.get()}\n\n"
    
    struk_text += "      PLN menyatakan struk ini sebagai bukti pembayaran yang sah.\n\n"
    
    struk_text += f"ADMIN BANK   : RP           {entry_admin.get():<15}\n"
    struk_text += f"TOTAL BAYAR  : RP           {entry_total.get():<15}\n\n"
    
    struk_text += " " * 34 + "Terima Kasih\n"
    struk_text += " " * 35 + "BANK BTN\n"
    struk_text += "     Informasi Hubungi Call Center 123 Atau Hub PLN Terdekat\n"
    
    if not struk_text.strip():
        messagebox.showwarning("Peringatan", "Tidak ada struk untuk disimpan.")
        return
    
    idpel = combo_idpel.get().strip()
    if not idpel:
        idpel = "struk_pln"
    
    default_filename = f"{idpel}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if REPORTLAB_AVAILABLE:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=default_filename + ".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("Text Files", "*.txt")]
        )
    else:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_filename + ".txt",
            filetypes=[("Text Files", "*.txt")]
        )
    
    if file_path:
        if file_path.endswith('.pdf') and REPORTLAB_AVAILABLE:
            try:
                from reportlab.pdfgen import canvas as pdf_canvas
                from reportlab.lib.pagesizes import A4
                
                c = pdf_canvas.Canvas(file_path, pagesize=A4)
                width, height = A4
                
                y_position = height - 50
                
                lines = struk_text.split('\n')
                for i, line in enumerate(lines):
                    if y_position < 50:
                        c.showPage()
                        y_position = height - 50
                    
                    # Deteksi baris yang perlu bold atau title
                    if "STRUK PEMBAYARAN TAGIHAN LISTRIK" in line:
                        c.setFont("Courier-Bold", 14)
                    elif any(keyword in line for keyword in ["NO REF", "PLN menyatakan", "TOTAL BAYAR"]):
                        c.setFont("Courier-Bold", 10)
                    else:
                        c.setFont("Courier", 10)
                    
                    c.drawString(50, y_position, line)
                    y_position -= 15
                
                c.save()
                messagebox.showinfo("Info", f"Struk berhasil disimpan sebagai PDF:\n{os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan PDF: {e}")
        else:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(struk_text)
            messagebox.showinfo("Info", "Struk berhasil disimpan sebagai TXT.")

def preview_print():
    # Ambil tarif dan daya dari combo_tarif_daya
    tarif_daya = combo_tarif_daya.get()
    if not tarif_daya or tarif_daya == "Pilih Tarif & Daya":
        tarif_daya = "N/A"
    
    # Generate struk text untuk print
    struk_text = "PT Bank Tabungan Negara (Persero) Tbk." + " " * 31 + "COPY\n"
    struk_text += "            STRUK PEMBAYARAN TAGIHAN LISTRIK\n\n"
    
    struk_text += f"IDPEL        : {combo_idpel.get():<30}BL/TH         : {entry_bulan.get()}\n"
    struk_text += f"NAMA         : {combo_nama.get():<30}STAND METER   : {entry_meter.get()}\n"
    struk_text += f"TARIF/DAYA   : {tarif_daya}\n"
    struk_text += f"RP TAG PLN   : RP           {entry_tagihan.get():<15}\n"
    struk_text += f"NO REF       : {entry_ref.get()}\n\n"
    
    struk_text += "      PLN menyatakan struk ini sebagai bukti pembayaran yang sah.\n\n"
    
    struk_text += f"ADMIN BANK   : RP           {entry_admin.get():<15}\n"
    struk_text += f"TOTAL BAYAR  : RP           {entry_total.get():<15}\n\n"
    
    struk_text += " " * 34 + "Terima Kasih\n"
    struk_text += " " * 35 + "BANK BTN\n"
    struk_text += "     Informasi Hubungi Call Center 123 Atau Hub PLN Terdekat\n"
    
    if not struk_text.strip():
        messagebox.showwarning("Peringatan", "Tidak ada struk untuk preview.")
        return
    
    preview_window = Toplevel(root)
    preview_window.title("Preview Print - Struk PLN")
    preview_window.geometry("800x900")
    preview_window.minsize(700, 800)
    preview_window.configure(bg="#f0f4f8")
    
    # Header preview
    header_preview = Frame(preview_window, bg=PRIMARY_COLOR, height=70)
    header_preview.pack(fill="x")
    header_preview.pack_propagate(False)
    
    Label(header_preview, text="🖨️ PREVIEW PRINT", 
          font=("Segoe UI", 16, "bold"), bg=PRIMARY_COLOR, fg="white").pack(pady=15)
    Label(header_preview, text="Periksa struk sebelum dicetak ke printer", 
          font=("Segoe UI", 9), bg=PRIMARY_COLOR, fg="#e0e7ff").pack()
    
    # Main container
    main_preview = Frame(preview_window, bg="#f0f4f8")
    main_preview.pack(fill="both", expand=True, padx=15, pady=15)
    
    # Card untuk preview
    preview_card = Frame(main_preview, bg="white", relief="flat")
    preview_card.pack(fill="both", expand=True, pady=(0, 10))
    
    # Shadow effect
    shadow = Frame(preview_card, bg="#d1d5db", height=2)
    shadow.pack(side="bottom", fill="x")
    
    # Area preview dengan scrollbar
    preview_content = Frame(preview_card, bg="white")
    preview_content.pack(fill="both", expand=True, padx=20, pady=20)
    
    scroll_frame = Frame(preview_content, bg="white")
    scroll_frame.pack(fill="both", expand=True)
    
    preview_scroll = Scrollbar(scroll_frame)
    preview_scroll.pack(side="right", fill="y")
    
    preview_text = Text(scroll_frame, font=("Courier New", 10), 
                       bg="#fafafa", relief="flat", bd=0,
                       highlightthickness=1, highlightbackground="#e5e7eb",
                       padx=20, pady=20, fg="#1f2937",
                       yscrollcommand=preview_scroll.set, wrap="none")
    preview_text.pack(side="left", fill="both", expand=True)
    preview_scroll.config(command=preview_text.yview)
    
    # Configure tags untuk formatting
    preview_text.tag_configure("bold", font=("Courier New", 10, "bold"))
    preview_text.tag_configure("title", font=("Courier New", 14, "bold"))
    preview_text.tag_configure("normal", font=("Courier New", 10))
    
    # Insert dengan formatting
    lines = struk_text.split('\n')
    for line in lines:
        if "STRUK PEMBAYARAN TAGIHAN LISTRIK" in line:
            preview_text.insert("end", line + "\n", "title")
        elif any(keyword in line for keyword in ["NO REF", "PLN menyatakan", "TOTAL BAYAR"]):
            preview_text.insert("end", line + "\n", "bold")
        else:
            preview_text.insert("end", line + "\n", "normal")
    
    preview_text.config(state="disabled")
    
    # Button frame dengan style modern
    button_preview = Frame(main_preview, bg="#f0f4f8")
    button_preview.pack(fill="x")
    
    def lanjut_cetak():
        preview_window.destroy()
        cetak_ke_printer(struk_text)
    
    btn_preview_style = {"font": ("Segoe UI", 10, "bold"), "cursor": "hand2",
                         "relief": "flat", "bd": 0, "padx": 25, "pady": 12}
    
    Button(button_preview, text="✓ Print ke Printer", command=lanjut_cetak, 
           bg=SUCCESS_COLOR, fg="white", **btn_preview_style).pack(side="left", padx=5)
    
    Button(button_preview, text="✕ Batal", command=preview_window.destroy, 
           bg="#6b7280", fg="white", **btn_preview_style).pack(side="left", padx=5)
    
    # Info footer
    Label(main_preview, text="💡 Tip: Pastikan printer sudah siap sebelum mencetak", 
          font=("Segoe UI", 8), bg="#f0f4f8", fg="#6b7280").pack(pady=(5, 0))

def cetak_ke_printer(isi=None):
    if isi is None:
        isi = text_struk.get("1.0", "end").strip()
    
    if not isi:
        messagebox.showwarning("Peringatan", "Tidak ada struk untuk dicetak.")
        return
    
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".txt", encoding="utf-8") as temp:
        temp.write(isi)
        temp_path = temp.name
    
    try:
        if platform.system() == "Windows":
            os.startfile(temp_path, "print")
        elif platform.system() == "Darwin":
            os.system(f"lp {temp_path}")
        else:
            os.system(f"lpr {temp_path}")
        messagebox.showinfo("Info", "Struk berhasil dikirim ke printer.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mencetak: {e}")

root = Tk()
root.title("Aplikasi Struk PLN Pascabayar")
root.geometry("1000x800")
root.minsize(900, 700)

# Konfigurasi tema warna modern
BG_COLOR = "#f0f4f8"
PRIMARY_COLOR = "#2563eb"
SECONDARY_COLOR = "#1e40af"
SUCCESS_COLOR = "#10b981"
DANGER_COLOR = "#ef4444"
TEXT_COLOR = "#1f2937"
CARD_BG = "#ffffff"

root.configure(bg=BG_COLOR)

# Style untuk ttk widgets
style = ttk.Style()
style.theme_use('clam')
style.configure('TCombobox', fieldbackground='white', background='white')

# Header dengan gradient effect - diperbaiki agar subtitle terlihat
header_frame = Frame(root, bg=PRIMARY_COLOR, height=85)
header_frame.pack(fill="x", side="top")
header_frame.pack_propagate(False)

title_label = Label(header_frame, text="⚡ STRUK PLN PASCABAYAR", 
                   font=("Segoe UI", 18, "bold"), 
                   bg=PRIMARY_COLOR, fg="white")
title_label.pack(pady=(15, 2))

subtitle_label = Label(header_frame, text="Sistem Pembayaran Tagihan Listrik", 
                      font=("Segoe UI", 9), 
                      bg=PRIMARY_COLOR, fg="#e0e7ff")
subtitle_label.pack(pady=(0, 10))

# Main container dengan canvas untuk scrolling
main_container = Frame(root, bg=BG_COLOR)
main_container.pack(fill="both", expand=True, padx=10, pady=10)

# Card untuk input form - dikompres lebih kecil
input_card = Frame(main_container, bg=CARD_BG, relief="flat", bd=0)
input_card.pack(padx=10, pady=(5, 5), fill="x")

# Tambahkan shadow effect dengan frame
shadow_frame = Frame(input_card, bg="#d1d5db", height=2)
shadow_frame.pack(side="bottom", fill="x")

input_header = Label(input_card, text="📋 Data Pelanggan", 
                    font=("Segoe UI", 11, "bold"), 
                    bg=CARD_BG, fg=TEXT_COLOR)
input_header.pack(anchor="w", padx=20, pady=(10, 5))

frame_input = Frame(input_card, bg=CARD_BG)
frame_input.pack(padx=20, pady=(0, 10), fill="x")

# Styling untuk labels
label_font = ("Segoe UI", 9)
entry_font = ("Segoe UI", 9)
entry_bg = "#ffffff"
entry_fg = "#1f2937"

# Fungsi untuk styling entry dengan hover effect
def create_entry(parent, width, **kwargs):
    entry = Entry(parent, width=width, font=entry_font, bg=entry_bg, fg=entry_fg,
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground="#e5e7eb", highlightcolor=PRIMARY_COLOR, **kwargs)
    
    def on_enter(e):
        entry.config(highlightbackground="#94a3b8")
    
    def on_leave(e):
        if entry != parent.focus_get():
            entry.config(highlightbackground="#e5e7eb")
    
    def on_focus_in(e):
        entry.config(highlightbackground=PRIMARY_COLOR, highlightcolor=PRIMARY_COLOR)
    
    def on_focus_out(e):
        entry.config(highlightbackground="#e5e7eb")
    
    entry.bind("<Enter>", on_enter)
    entry.bind("<Leave>", on_leave)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    
    return entry

# Row 0 - spacing dikurangi
Label(frame_input, text="ID Pelanggan", font=label_font, bg=CARD_BG, fg=TEXT_COLOR).grid(row=0, column=0, sticky="w", pady=5)
combo_idpel = ttk.Combobox(frame_input, width=25, font=entry_font)
combo_idpel.grid(row=0, column=1, pady=5, padx=(0, 15), sticky="ew", ipady=3)
combo_idpel['values'] = [f"{idpel} - {nama}" for idpel, nama in DATA_PELANGGAN]
combo_idpel.bind('<KeyRelease>', cari_pelanggan)
combo_idpel.bind('<<ComboboxSelected>>', pilih_pelanggan)

Label(frame_input, text="No. Struk", font=label_font, bg=CARD_BG, fg=TEXT_COLOR).grid(row=0, column=2, sticky="w", pady=5, padx=(15, 0))
Label(frame_input, text="2", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=PRIMARY_COLOR).grid(row=0, column=3, sticky="w", pady=5)

# Row 1
Label(frame_input, text="Nama Pelanggan", font=label_font, bg=CARD_BG, fg=TEXT_COLOR).grid(row=1, column=0, sticky="w", pady=5)
combo_nama = ttk.Combobox(frame_input, width=25, font=entry_font)
combo_nama.grid(row=1, column=1, pady=5, padx=(0, 15), sticky="ew", ipady=3)
combo_nama['values'] = [f"{nama} - {idpel}" for idpel, nama in DATA_PELANGGAN]
combo_nama.bind('<KeyRelease>', cari_nama)
combo_nama.bind('<<ComboboxSelected>>', pilih_nama)

Label(frame_input, text="Tanggal", font=label_font, bg=CARD_BG, fg=TEXT_COLOR).grid(row=1, column=2, sticky="w", pady=5, padx=(15, 0))
entry_tanggal = create_entry(frame_input, 22)
entry_tanggal.grid(row=1, column=3, pady=5, ipady=5, sticky="ew")
entry_tanggal.insert(0, datetime.now().strftime("%d/%m/%Y"))

# Row 2 - Tarif/Daya dengan dropdown seperti Nama Pelanggan
Label(frame_input, text="Tarif/Daya", font=label_font, bg=CARD_BG, fg=TEXT_COLOR).grid(row=2, column=0, sticky="w", pady=5)

combo_tarif_daya = ttk.Combobox(frame_input, width=25, font=entry_font)
combo_tarif_daya['values'] = [f"{tarif} - {daya}" for tarif, daya in DATA_TARIF_DAYA]
combo_tarif_daya.set("Pilih Tarif & Daya")
combo_tarif_daya.grid(row=2, column=1, pady=5, padx=(0, 15), sticky="ew", ipady=3)
combo_tarif_daya.bind('<<ComboboxSelected>>', pilih_tarif_daya)

Label(frame_input, text="Bulan/Tahun", font=label_font, bg=CARD_BG, fg=TEXT_COLOR).grid(row=2, column=2, sticky="w", pady=5, padx=(15, 0))
entry_bulan = create_entry(frame_input, 22)
entry_bulan.grid(row=2, column=3, pady=5, ipady=5, sticky="ew")

# Row 3
Label(frame_input, text="Tagihan PLN (Rp)", font=label_font, bg=CARD_BG, fg=TEXT_COLOR).grid(row=3, column=0, sticky="w", pady=5)
entry_tagihan = create_entry(frame_input, 27)
entry_tagihan.grid(row=3, column=1, pady=5, padx=(0, 15), ipady=5, sticky="ew")
entry_tagihan.bind('<KeyRelease>', hitung_total)

Label(frame_input, text="Stand Meter", font=label_font, bg=CARD_BG, fg=TEXT_COLOR).grid(row=3, column=2, sticky="w", pady=5, padx=(15, 0))
entry_meter = create_entry(frame_input, 22)
entry_meter.grid(row=3, column=3, pady=5, ipady=5, sticky="ew")

# Row 4
Label(frame_input, text="Referensi", font=label_font, bg=CARD_BG, fg=TEXT_COLOR).grid(row=4, column=0, sticky="w", pady=5)
entry_ref = create_entry(frame_input, 27)
entry_ref.grid(row=4, column=1, pady=5, padx=(0, 15), ipady=5, sticky="ew")

Label(frame_input, text="Admin Bank (Rp)", font=label_font, bg=CARD_BG, fg=TEXT_COLOR).grid(row=4, column=2, sticky="w", pady=5, padx=(15, 0))
entry_admin = create_entry(frame_input, 22)
entry_admin.grid(row=4, column=3, pady=5, ipady=5, sticky="ew")
entry_admin.bind('<KeyRelease>', hitung_total)

# Separator line
separator = Frame(frame_input, height=1, bg="#e5e7eb")
separator.grid(row=5, column=0, columnspan=4, sticky="ew", pady=8)

# Row 5 - Total Bayar dengan styling khusus
total_label = Label(frame_input, text="💰 Total Bayar", font=("Segoe UI", 10, "bold"), bg=CARD_BG, fg=SUCCESS_COLOR)
total_label.grid(row=6, column=0, sticky="w", pady=5)

entry_total = Entry(frame_input, width=27, font=("Segoe UI", 11, "bold"), 
                   bg="#f0fdf4", fg="#15803d", relief="flat", bd=0,
                   highlightthickness=1, highlightbackground="#86efac",
                   highlightcolor="#22c55e",
                   disabledbackground="#f0fdf4", disabledforeground="#15803d")
entry_total.grid(row=6, column=1, pady=5, padx=(0, 15), ipady=6, sticky="ew")
entry_total.config(state="readonly")

# Info label untuk total
info_label = Label(frame_input, text="✓ Otomatis terhitung", font=("Segoe UI", 7), 
                  bg=CARD_BG, fg="#10b981")
info_label.grid(row=6, column=2, columnspan=2, sticky="w", pady=5, padx=(15, 0))

frame_input.columnconfigure(1, weight=1)
frame_input.columnconfigure(3, weight=1)

# Tombol Aksi dengan style modern - spacing dikurangi
button_frame = Frame(main_container, bg=BG_COLOR)
button_frame.pack(pady=8)

btn_style = {"font": ("Segoe UI", 10, "bold"), "cursor": "hand2", 
             "relief": "flat", "bd": 0, "padx": 20, "pady": 10}

btn_cetak = Button(button_frame, text="📄 Generate Struk", command=cetak_struk, 
                   bg=PRIMARY_COLOR, fg="white", **btn_style)
btn_cetak.grid(row=0, column=0, padx=5)

btn_simpan = Button(button_frame, text="💾 Simpan PDF", command=simpan_struk, 
                    bg=SUCCESS_COLOR, fg="white", **btn_style)
btn_simpan.grid(row=0, column=1, padx=5)

btn_print = Button(button_frame, text="🖨️ Print", command=preview_print, 
                   bg=SECONDARY_COLOR, fg="white", **btn_style)
btn_print.grid(row=0, column=2, padx=5)

# Card untuk preview struk dengan ukuran lebih besar
preview_card = Frame(main_container, bg=CARD_BG, relief="flat", bd=0)
preview_card.pack(padx=10, pady=(0, 5), fill="both", expand=True)

preview_header = Label(preview_card, text="📋 Preview Struk", 
                      font=("Segoe UI", 11, "bold"), 
                      bg=CARD_BG, fg=TEXT_COLOR)
preview_header.pack(anchor="w", padx=20, pady=(10, 5))

text_frame = Frame(preview_card, bg=CARD_BG)
text_frame.pack(padx=20, pady=(0, 10), fill="both", expand=True)

scrollbar = Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")

text_struk = Text(text_frame, width=100, height=30, font=("Courier New", 10),
                 yscrollcommand=scrollbar.set, wrap="none", 
                 bg="#fafafa", relief="flat", bd=0,
                 highlightthickness=1, highlightbackground="#e5e7eb",
                 padx=15, pady=15, fg="#1f2937", 
                 insertbackground=PRIMARY_COLOR, selectbackground="#dbeafe")
text_struk.pack(side="left", fill="both", expand=True, padx=(0, 5))
scrollbar.config(command=text_struk.yview)

# Footer
footer_frame = Frame(root, bg=BG_COLOR)
footer_frame.pack(fill="x", side="bottom", pady=5)

btn_tutup = Button(footer_frame, text="❌ Tutup Aplikasi", command=root.quit, 
                   bg=DANGER_COLOR, fg="white", 
                   font=("Segoe UI", 10, "bold"), cursor="hand2",
                   relief="flat", bd=0, padx=30, pady=8)
btn_tutup.pack(pady=5)

Label(footer_frame, text="© 2024 Aplikasi Struk PLN | Version 1.0", 
      font=("Segoe UI", 8), bg=BG_COLOR, fg="#6b7280").pack()

root.mainloop()
