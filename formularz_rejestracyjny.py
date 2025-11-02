import tkinter as tk

class FormField:
    def __init__(self, root, text: str):
        self.label = tk.Label(root, text = text)
        self.entry = tk.Entry(root, width = 30) 

    def pack(self, row):
        self.label.grid(row=row, column=0, padx=5, pady=5)
        self.label.grid(row=row + 1, column=1, padx=5, pady=5)

def zarejestruj():
    print(f"""
Imie:     {entry_imie.get()}
E-Mail:   {entry_email.get()}
Wiek:     {stan_wiek.get()}
Ksiazki:  {'tak' if ksiazki_var.get() else 'nie'}
Sport:    {'tak' if sport_var.get() else 'nie'}
Uwagi:    {text_uwagi.get('1.0', 'end-1c')}""")

root = tk.Tk()
root.title("Formularz Rejestracyjny")
root.geometry("800x700")

stan_wiek = tk.StringVar(value="18-30")

label_imie = tk.Label(root, text="Imie")
label_email = tk.Label(root, text="Email")
label_wiek = tk.Label(root, text="Wiek")
label_zainteresowania = tk.Label(root, text="Zainteresowania")
label_uwagi = tk.Label(root, text="Uwagi")
entry_imie = tk.Entry(root, width = 30)
entry_email = tk.Entry(root, width = 30)

wiek_1 = tk.Radiobutton(root, text="18-30", variable=stan_wiek, value="18-30")
wiek_2 = tk.Radiobutton(root, text="19-50", variable=stan_wiek, value="19-50")
wiek_3 = tk.Radiobutton(root, text="50+", variable=stan_wiek, value="50+")

ksiazki_var = tk.IntVar()
sport_var = tk.IntVar()
zaint_1 = tk.Checkbutton(root, text="Książki", variable=ksiazki_var)
zaint_2 = tk.Checkbutton(root, text="Sport", variable=sport_var)

text_uwagi = tk.Text(root)

label_imie.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_imie.grid(row=0, column=1, padx=5, pady=5    )

label_email.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_email.grid(row=1, column=1, padx=5, pady=5    )

label_wiek.grid(row=2, column=0, padx=5, pady=5, sticky="e")
wiek_1.grid(row=2, column=1, padx=5, pady=5)
wiek_2.grid(row=2, column=2, padx=5, pady=5)
wiek_3.grid(row=2, column=3, padx=5, pady=5)

label_zainteresowania.grid(row=3, column=0, padx=5, pady=5, sticky="e")
zaint_1.grid(row=3, column=1, padx=5, pady=5)
zaint_2.grid(row=3, column=2, padx=5, pady=5)

label_uwagi.grid(row=4, column=0, padx=5, pady=5, sticky="e")
text_uwagi.grid(row=4, column=3, sticky="w")

tk.Button(root, text="Zarejestruj", command=zarejestruj).grid(row=5, column=0)


root.mainloop()
