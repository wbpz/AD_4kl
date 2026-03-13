#!/bin/python3
import json
import customtkinter as ctk
import tkinter.ttk as ttk

SETTINGS_FILE = "settings.json"

def set_theme(theme: string) -> None:
    combobox.set(theme)
    ctk.set_appearance_mode(theme)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        f.write(json.dumps({ "theme": theme }))

def read_settings():
    file = open(SETTINGS_FILE, "r", encoding="utf-8")
    if not file: return {}
    return json.loads(file.read())

settings = read_settings()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Aplikacja Python UI")

combobox = ctk.CTkOptionMenu(master=app,
                             values=["light", "dark"],
                             command=set_theme)

if settings: set_theme(settings["theme"])
combobox.pack(pady=20)

ctk.CTkButton(app, text="x").pack()
ctk.CTkEntry(app).pack()
ctk.CTkCheckBox(app, text="checkbox").pack()
ctk.CTkTextbox(app).pack()

app.mainloop()
