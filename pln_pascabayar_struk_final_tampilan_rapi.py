
from tkinter import Tk, Frame, Label, Entry, Text, Button, filedialog, messagebox, font
from datetime import datetime
import tempfile
import os
import platform

def cetak_struk():
    left = [
        f"IDPEL       : {entry_idpel.get()}",
        f"NAMA        : {entry_nama.get()}",
        f"TARIF/DAYA  : {entry_tarif.get()}/{entry_daya.get()}",
        f"RP TAG PLN  : Rp. {entry_tagihan.get()}",
        f"REF         : {entry_ref.get()}"
    ]
    right = [
        f"NO STRUK     : 2",
        f"TANGGAL      : {entry_tanggal.get()}",
        f"BLN/TH       : {entry_bulan.get()}",
        f"STAND METER  : {entry_meter.get()}",
        ""
    ]

    struk = "STRUK BUKTI PEMBAYARAN TAGIHAN LISTRIK\n\n"

    for l, r in zip(left, right):
        struk += f"{l:<45}{r}\n"

    struk += (
        "\n"
        "             PLN menyatakan struk ini sebagai bukti pembayaran yang sah\n\n"
        f"ADMIN BANK  : Rp. {entry_admin.get()}\n"
        f"RP BAYAR    : Rp. {entry_total.get()}\n\n"
        "                             TERIMA KASIH\n"
        "        Rincian tagihan dapat dilihat di www.pln.co.id atau PLN terdekat\n"
        "                            INFORMASI HUB: 123\n"
    )

    text_struk.delete("1.0", "end")
    text_struk.insert("end", struk)

def simpan_struk():
    isi = text_struk.get("1.0", "end").strip()
    if not isi:
        messagebox.showwarning("Peringatan", "Tidak ada struk untuk disimpan.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(isi)
        messagebox.showinfo("Info", "Struk berhasil disimpan.")

def cetak_ke_printer():
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
root.title("Struk PLN Pascabayar")
root.geometry("840x1050")

frame_input = Frame(root)
frame_input.pack(padx=10, pady=10)

Label(frame_input, text="IDPEL").grid(row=0, column=0, sticky="w")
entry_idpel = Entry(frame_input, width=25)
entry_idpel.grid(row=0, column=1)

Label(frame_input, text="No Struk").grid(row=0, column=2, sticky="w")
Label(frame_input, text="2").grid(row=0, column=3, sticky="w")

Label(frame_input, text="Nama").grid(row=1, column=0, sticky="w")
entry_nama = Entry(frame_input, width=25)
entry_nama.grid(row=1, column=1)

Label(frame_input, text="Tanggal").grid(row=1, column=2, sticky="w")
entry_tanggal = Entry(frame_input, width=20)
entry_tanggal.grid(row=1, column=3)
entry_tanggal.insert(0, datetime.now().strftime("%d/%m/%Y"))

Label(frame_input, text="Tarif").grid(row=2, column=0, sticky="w")
entry_tarif = Entry(frame_input, width=10)
entry_tarif.grid(row=2, column=1, sticky="w")

Label(frame_input, text="Daya").grid(row=2, column=1, sticky="e")
entry_daya = Entry(frame_input, width=10)
entry_daya.grid(row=2, column=2, sticky="w")

Label(frame_input, text="BLN/TH").grid(row=2, column=2, sticky="e")
entry_bulan = Entry(frame_input, width=20)
entry_bulan.grid(row=2, column=3)

Label(frame_input, text="Rp Tagihan").grid(row=3, column=0, sticky="w")
entry_tagihan = Entry(frame_input, width=25)
entry_tagihan.grid(row=3, column=1)

Label(frame_input, text="Stand Meter").grid(row=3, column=2, sticky="w")
entry_meter = Entry(frame_input, width=20)
entry_meter.grid(row=3, column=3)

Label(frame_input, text="REF").grid(row=4, column=0, sticky="w")
entry_ref = Entry(frame_input, width=25)
entry_ref.grid(row=4, column=1)

Label(frame_input, text="Admin Bank").grid(row=5, column=0, sticky="w")
entry_admin = Entry(frame_input, width=25)
entry_admin.grid(row=5, column=1)

Label(frame_input, text="Total Bayar").grid(row=6, column=0, sticky="w")
entry_total = Entry(frame_input, width=25)
entry_total.grid(row=6, column=1)

# Tombol Aksi
button_frame = Frame(root)
button_frame.pack(pady=10)

Button(button_frame, text="Cetak", width=18, command=cetak_struk).grid(row=0, column=0, padx=5)
Button(button_frame, text="Simpan ke File", width=18, command=simpan_struk).grid(row=0, column=1, padx=5)
Button(button_frame, text="Cetak ke Printer", width=18, command=cetak_ke_printer).grid(row=0, column=2, padx=5)

# Area teks struk dengan judul font besar
Label(root, text="STRUK BUKTI PEMBAYARAN TAGIHAN LISTRIK", font=("Courier New", 16, "bold")).pack()
text_struk = Text(root, width=110, height=50, font=("Courier New", 10))
text_struk.pack(padx=10, pady=10)

Button(root, text="Tutup", width=20, command=root.quit).pack(pady=5)

root.mainloop()
