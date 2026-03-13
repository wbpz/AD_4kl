#!/bin/python3
import customtkinter as ctk
import tkinter.ttk as ttk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Aplikacja Python UI")

combobox = ctk.CTkOptionMenu(master=app,
                             values=["light", "dark"],
                             command=ctk.set_appearance_mode)
combobox.set("dark")
combobox.pack(pady=20)

app.mainloop()
