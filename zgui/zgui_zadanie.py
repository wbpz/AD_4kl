import tkinter as tk
from tkinter import ttk

def show_selection(event):
    """Funkcja obsługująca zdarzenie wyboru w Combobox."""
    print(f"Wybrano opcję: {combo.get()}")

def start_progress():
    """Funkcja symulująca i sterująca paskiem postępu."""
    pbar.start(15)
    root.after(3000, stop_progress)
    
def stop_progress():
    """Funkcja zatrzymująca pasek postępu."""   
    pbar.stop()

root = tk.Tk()
root.title("Zaawansowane GUI Ttk")

notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=10, expand=True, fill="both")

tab1 = ttk.Frame(notebook, padding="10")
tab2 = ttk.Frame(notebook, padding="10")

notebook.add(tab1, text="Wygląd")
notebook.add(tab2, text="Prywatność")

ttk.Label(tab1, text="Wybierz motyw:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
label = ttk.Label(tab1, text="Label")
label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

styles = ["Jasny", "Ciemny", "Systemowy"]
combo = ttk.Combobox(tab1, values=styles, state="readonly")
combo.current(0) # Ustawienie domyślnej wartości
combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

contrast = tk.BooleanVar()
ttk.Checkbutton(tab1, var=contrast, text="Włącz wysoki kontrast").grid(row=1, column=0, padx=5, pady=5)

combo.bind("<<ComboboxSelected>>", show_selection)

pbar = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
pbar.pack(pady=10)

data = tk.StringVar(value="Wszystkie")
ttk.Radiobutton(tab2, text="Wszystkie", value="all", var=data).pack(padx=5, pady=5)
ttk.Radiobutton(tab2, text="Anonimowe", val="anon", var=data).pack(padx=5, pady=5)
ttk.Radiobutton(tab2, text="Żadne", value="none", var=data).pack(padx=5, pady=5)

ttk.Button(root, text="Start Procesu", command=start_progress).pack(side="left", padx=5)
ttk.Button(root, text="Stop Procesu", command=stop_progress).pack(side="left", padx=5)

root.mainloop()
