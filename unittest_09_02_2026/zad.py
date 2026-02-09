import tkinter as tk

ERROR = "Błąd danych"

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.lhs = tk.Entry(self)
        self.rhs = tk.Entry(self)
        self.result = tk.Label(self)
        self.submit = tk.Button(self, text="Oblicz", command=lambda: self.result.config(text=self.calculate()))

        self.lhs.pack()
        self.rhs.pack()
        self.submit.pack()
        self.result.pack()

    def calculate(self) -> string:
        lhs = self.lhs.get()
        rhs = self.rhs.get()
        try:
            lhs = int(lhs)
            rhs = int(rhs)
            return f"{lhs + rhs}"
        except:
            return ERROR

def main(): 
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
