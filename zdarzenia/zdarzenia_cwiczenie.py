import tkinter as tk

root = tk.Tk()
root.title("Zdarzenia Cwiczenie")
root.geometry("600x450")

label = tk.Label(root, text="Pozycja: (?, ?)", padx=10, pady=10)
label.pack()

root.bind("<Motion>", lambda e: label.config(text=f"Pozycja: ({e.x}. {e.y})"))


root.mainloop()
    