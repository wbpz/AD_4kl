import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# --- FUNKCJE BAZY DANYCH (jak wyżej w sekcji 2) ---
# (polacz_z_baza, dodaj_dane, pobierz_wszystkie_produkty)
def polacz_z_baza():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mojabaza"
        )
        return mydb
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd Połączenia", f"Nie można połączyć się z bazą danych: {err}")
        return None


def dodaj_dane(nazwa, ilosc):
    conn = polacz_z_baza()
    if conn is None: return

    cursor = conn.cursor()
    sql = "INSERT INTO produkty (nazwa_produktu, ilosc) VALUES (%s, %s)"
    val = (nazwa, ilosc)
    try:
        cursor.execute(sql, val)
        conn.commit()
        messagebox.showinfo("Sukces", "Produkt dodany pomyślnie.")
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania: {err}")
    finally:
        cursor.close()
        conn.close()

def pobierz_wszystkie_produkty():
    conn = polacz_z_baza()
    if conn is None: return []

    cursor = conn.cursor()
    sql = "SELECT id, nazwa_produktu, ilosc FROM produkty"
    try:
        cursor.execute(sql)
        wyniki = cursor.fetchall() # Zwraca listę tupli
        return wyniki
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas pobierania: {err}")
        return []
    finally:
        cursor.close()
        conn.close()
        
def aktualizuj_ilosc(id_produktu, nowa_ilosc):
    sql = "UPDATE produkty SET ilosc = %s WHERE id = %s"
    conn = polacz_z_baza()
    if conn is None: return
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (nowa_ilosc, id_produktu))
        conn.commit()
        messagebox.showinfo("Sukces", "Pomyślnie zaaktualizowano produkt")
        pobierz_wszystkie_produkty()
        odswiez_treeview(tree)
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania: {err}")
    finally:
        cursor.close()
        conn.close()


# --- FUNKCJE GUI ---

def odswiez_treeview(tree):
    for item in tree.get_children():
        tree.delete(item) # Usuń stare wiersze
    dane = pobierz_wszystkie_produkty()
    for wiersz in dane:
        tree.insert('', tk.END, values=wiersz)

def obsluga_dodawania(nazwa_var, ilosc_var, tree):
    nazwa = nazwa_var.get()
    try:
        ilosc = int(ilosc_var.get())
    except ValueError:
        messagebox.showerror("Błąd", "Ilość musi być liczbą całkowitą.")
        return

    if nazwa and ilosc >= 0:
        dodaj_dane(nazwa, ilosc)
        odswiez_treeview(tree) # Odśwież widok po dodaniu
        nazwa_var.set(""); ilosc_var.set("") # Wyczyść pola
    else:
        messagebox.showwarning("Uwaga", "Wypełnij poprawnie wszystkie pola.")

# --- KONFIGURACJA GŁÓWNEGO OKNA ---

root = tk.Tk()
root.title("System Zarządzania Magazynem")

# Zmienne kontrolne dla pól wejściowych
nazwa_produktu_var = tk.StringVar()
ilosc_var = tk.StringVar()

# --- Sekcja formularza (INPUT) ---
form_frame = ttk.Frame(root, padding="10")
form_frame.pack(padx=10, pady=10, fill='x')

ttk.Label(form_frame, text="Nazwa Produktu:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=nazwa_produktu_var, width=30).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Ilość:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=ilosc_var, width=10).grid(row=1, column=1, padx=5, pady=5, sticky='w')

dodaj_btn = ttk.Button(form_frame, text="Dodaj Produkt",
    command=lambda: obsluga_dodawania(nazwa_produktu_var, ilosc_var, tree))
dodaj_btn.grid(row=2, column=0, columnspan=2, pady=10)

ttk.Label(form_frame, text="ID:").grid(row=3, column=0, padx=5, pady=5)
upd_id = tk.StringVar()
ttk.Entry(form_frame, textvariable=upd_id, width=10).grid(row=3, column=1, padx=5, pady=5, sticky='w')

ttk.Label(form_frame, text="Ilosc:").grid(row=4, column=0, padx=5, pady=5)
upd_ilosc_var = tk.StringVar()
ttk.Entry(form_frame, textvariable=upd_ilosc_var, width=10).grid(row=4, column=1, padx=5, pady=5, sticky='w')

dodaj_btn = ttk.Button(form_frame, text="Aktualizuj ilość",
    command=lambda: aktualizuj_ilosc(upd_id.get(), upd_ilosc_var.get()))
dodaj_btn.grid(row=5, column=0, columnspan=2, pady=10)

# --- Sekcja wyświetlania danych (Treeview) ---

columns = ('id', 'nazwa', 'ilosc')
tree = ttk.Treeview(root, columns=columns, show='headings')

tree.heading('id', text='ID')
tree.column('id', width=50, anchor='center')
tree.heading('nazwa', text='Nazwa Produktu')
tree.column('nazwa', width=250)
tree.heading('ilosc', text='Ilość')
tree.column('ilosc', width=80, anchor='center')

tree.pack(pady=10, padx=10, fill='both', expand=True)

# Początkowe załadowanie danych
odswiez_treeview(tree)

root.mainloop()