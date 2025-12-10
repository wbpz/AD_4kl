import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="filmy"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd Połączenia", f"Nie można połączyć się z bazą danych: {err}")
        return None

def display_data():
    db = get_connection()
    if db == None: return
    cursor = db.cursor()
    sql = "SELECT id, tytul, rezyser, rok, ocena from filmy"
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for item in tree.get_children(): tree.delete(item)
        for row in rows: tree.insert('', tk.END, values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Error: {err}")
    finally:
        cursor.close()
        db.close()


def insert_new_film():
    db = get_connection()
    if db == None: return
    cursor = db.cursor()
    sql = "INSERT INTO filmy (tytul, rezyser, rok, ocena) VALUES (%s, %s, %s, %s)"
    values = (tytul_var.get(), rezys_var.get(), rok_var.get(), ocena_var.get())
    try:
        cursor.execute(sql, values)
        db.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Error: {err}")
    finally:
        cursor.close()
        db.close()
        display_data()

def edit_film():
    db = get_connection()
    if db == None: return
    cursor = db.cursor()
    sql = "UPDATE filmy SET tytul = %s, rezyser = %s, rok = %s, ocena = %s WHERE id = %s;"
    values = (tytul_var.get(), rezys_var.get(), rok_var.get(), ocena_var.get(), id_var.get())
    try:
        cursor.execute(sql, values)
        db.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Error: {err}")
    finally:
        cursor.close()
        db.close()
        display_data()
        
def del_film():
    db = get_connection()
    if db == None: return
    cursor = db.cursor()
    sql = "DELETE FROM filmy WHERE id = %s;"
    values = (id_var.get(), )
    try:
        cursor.execute(sql, values)
        db.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Błąd", f"Error: {err}")
    finally:
        cursor.close()
        db.close()
        display_data()

print("Hello world")

root = tk.Tk()
root.title("title")

form_frame = ttk.Frame(root, padding="10")
form_frame.pack(padx=10, pady=10, fill="x")

tytul_var = tk.StringVar()
rezys_var = tk.StringVar()
rok_var = tk.StringVar()
ocena_var = tk.StringVar()
id_var = tk.StringVar()

ttk.Label(form_frame, text="Tytuł").grid(row=0, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=tytul_var, width=30).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Reżyser").grid(row=1, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=rezys_var, width=30).grid(row=1, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Rok").grid(row=2, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=rok_var, width=30).grid(row=2, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Ocena").grid(row=3, column=0, padx=5, pady=5, sticky='w')
ttk.Entry(form_frame, textvariable=ocena_var, width=30).grid(row=3, column=1, padx=5, pady=5)

ttk.Button(form_frame, command = insert_new_film, text="Dodaj").grid(row=4, padx=5, pady=5)

ttk.Label(form_frame, text="ID").grid(row=5, column=0, padx=5, pady=5)
ttk.Entry(form_frame, textvariable=id_var, width=30).grid(row=5, column=1, padx=5, pady=5, sticky='w')
ttk.Button(form_frame, command = edit_film, text="Edytuj").grid(row=5, column=3, padx=5, pady=5)
ttk.Button(form_frame, command = del_film, text="Usuń").grid(row=5, column=4, padx=5, pady=5)

columns = ('id', 'nazwa', 'rezyser', 'rok', 'ocena')
tree = ttk.Treeview(root, columns=columns, show='headings')

tree.heading('id', text='ID')
tree.column('id', width=50, anchor='center')
tree.heading('nazwa', text='Nazwa Filmu')
tree.column('nazwa', width=250)
tree.heading('rezyser', text='Reżyser')
tree.column('rezyser', width=80, anchor='center')
tree.heading('rok', text='Rok')
tree.column('rok', width=80, anchor='center')
tree.heading('ocena', text='ocena')
tree.column('ocena', width=80, anchor='center')

tree.pack(pady=10, padx=10, fill='both', expand=True)

display_data()

root.mainloop()
