import tkinter as tk
from tkinter import ttk, messagebox

class KwadratModel:
    def __init__(self):
        self._wartosc = 0

    def get_wartosc(self):
        return self._wartosc

    def ustaw_wartosc(self, wartosc):
        self._wartosc = wartosc

class KwadratView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Kwadrat MVC w Pythonie")
        self.geometry("300x150")

        self.controller = controller
        
        self.licznik_var = tk.StringVar(value="Kwadrat: 0")

        self._utworz_widzety()
        
    def _utworz_widzety(self):
        self.licznik_label = ttk.Label(self, textvariable=self.licznik_var, font=("Arial", 16))
        self.licznik_label.pack(pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        self.kwadrat_entry = ttk.Entry(button_frame, text="Wartość  ")
        self.kwadrat_entry.pack()

        self.submit_button = ttk.Button(button_frame, text="Oblicz", command=self.controller.ustaw_wartosc)
        self.submit_button.pack()


    def ustaw_wartosc_licznika(self, nowa_wartosc):
        self.licznik_var.set(f"Kwadrat: {nowa_wartosc}")

class KwadratController:
    def __init__(self, model, view):
        self.model = model
        self.view = view 

    def aktualizuj_view(self):
        wartosc = self.model.get_wartosc()
        self.view.ustaw_wartosc_licznika(wartosc)

    def ustaw_wartosc(self):
        try:
            value = int(self.view.kwadrat_entry.get())
        except:
            messagebox.showerror("", "Należy wpisać liczbę")
            return
        self.model.ustaw_wartosc(value * value)
        self.aktualizuj_view()

    def obsluz_reset(self):
        self.model.resetuj()
        self.aktualizuj_view()

# ====================================================================
# 4. PUNKT STARTOWY
# ====================================================================

if __name__ == "__main__":
    model = KwadratModel()

    controller_instance = KwadratController(model, view=None) 
    
    view_instance = KwadratView(controller_instance)    
    
    controller_instance.view = view_instance
    controller_instance.aktualizuj_view()

    view_instance.mainloop()
