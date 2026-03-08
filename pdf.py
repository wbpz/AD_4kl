import tkinter as tk
import reportlab
import datetime
from tkinter import filedialog, messagebox
from reportlab.platypus.tables import Table
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def generuj_pdf():
    # 1. Pobieranie danych z interfejsu
    nazwa = entry_nazwa.get()
    netto = entry_netto.get()
    vat = entry_vat.get()

    imie = entry_imie.get()
    notatka = text_notatka.get("1.0", tk.END).strip()

    if not nazwa or not netto or not vat or not imie or not notatka:
        messagebox.showerror("Błąd", "")
        return

    try:
        netto = int(netto)
    except Exception:
        messagebox.showerror("Błąd", "Netto powinno być liczbą")
        return

    try:
        vat = int(vat)
    except Exception:
        messagebox.showerror("Błąd", "Netto powinno być liczbą")
        return

    brutto = netto + (netto * vat) / 100

    # 2. Wybór lokalizacji zapisu
    sciezka = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Pliki PDF", "*.pdf")],
        title="Zapisz raport jako..."
    )

    if not sciezka: return


    time = datetime.date.today().strftime("%d %B %Y")

    c = canvas.Canvas(sciezka, pagesize=A4)
    c.setFont("Helvetica", 16)
    szerokosc, wysokosc = A4
    

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, wysokosc - 50, "RAPORT GENEROWANY Z TKINTER")
    
    c.line(100, wysokosc - 60, 500, wysokosc - 60)

    c.setFont("Helvetica", 12)
    c.drawString(100, wysokosc - 100, f"Użytkownik: {imie}")
    
    c.drawString(100, wysokosc - 130, "Treść notatki:")
    
    tekst_obj = c.beginText(100, wysokosc - 150)
    tekst_obj.setFont("Helvetica", 10)
    tekst_obj.textLines(notatka)
    c.drawText(tekst_obj)

    data = [
        ["netto", "brutto", "vat"],
        [netto, brutto, vat]
    ]
    table = Table(data)
    x = szerokosc
    y = wysokosc
    table.wrapOn(c, x, y)
    table.drawOn(c, 100, wysokosc - 250)

    c.drawString(100, wysokosc - 300, f"czas: {time}")

    c.save()
    messagebox.showinfo("Sukces", "Plik PDF został utworzony pomyślnie!")

root = tk.Tk()
root.title("Generator PDF")
root.geometry("400x400")

tk.Label(root, text="Imię i Nazwisko:", font=("Arial", 10, "bold")).pack(pady=5)
entry_imie = tk.Entry(root, width=40)
entry_imie.pack(pady=5)

tk.Label(root, text="Treść notatki:", font=("Arial", 10, "bold")).pack(pady=5)
text_notatka = tk.Text(root, width=40, height=10)
text_notatka.pack(pady=5)

tk.Label(root, text="Nazwa produktu").pack(pady=5)
entry_nazwa = tk.Entry(root, width=40)
entry_nazwa.pack(pady=5)

tk.Label(root, text="Cena netto").pack(pady=5)
entry_netto = tk.Entry(root, width=40)
entry_netto.pack(pady=5)

tk.Label(root, text="Stawka VAT").pack(pady=5)
entry_vat = tk.Entry(root, width=40)
entry_vat.pack(pady=5)

btn_export = tk.Button(root, text="Eksportuj do PDF", command=generuj_pdf, bg="#27ae60", fg="white", padx=20)
btn_export.pack(pady=20)

root.mainloop()
