import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.entry = tk.Entry(self)
        self.entry.pack()
        self.label = tk.Label(self, text="Czekam...")
        self.label.pack()

        self.btn = tk.Button(self, text="Powitaj", command=self.say_hello)
        self.btn.pack()

        self.clear = tk.Button(self, text="Wyczyść", command=self.clear)
        self.clear.pack()

    def say_hello(self):
        name = self.entry.get()
        self.label.config(text=f"Witaj, {name}!")

    def clear(self):
        self.label.config(text="")
        self.entry.delete(0, tk.END)


def main(): 
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
