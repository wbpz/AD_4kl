import tkinter as tk
from tkinter import messagebox

def pokaz_dane():
    metry = pole_metry.get()
    as_number = 0
    try:
        as_number = int(metry)
    except ValueError:
        label_result.config(text="Invalid number")
        return
    label_result.config(text=f"{str(as_number * 3.28084)} stopy")    

root = tk.Tk()
root.title("Przykładowe Kontrolki Tkinter")
root.geometry("400x350")

stan_aktywny = tk.IntVar()

tk.Label(root, text="Podaj metry:").pack()

# Entry dla imienia
pole_metry = tk.Entry(root, width=30)
pole_metry.pack()
przycisk_akcja = tk.Button(root, text="Metry na stopy", command=pokaz_dane, bg="#4CAF50", fg="white", font=('Arial', 10, 'bold'))
przycisk_akcja.pack()
label_result = tk.Label(root, text="0.0 stopy")
label_result.pack()
root.mainloop()
