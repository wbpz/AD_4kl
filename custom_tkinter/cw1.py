#!/bin/python3
import customtkinter as ctk
import tkinter.ttk as ttk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Aplikacja Python UI")

btn = ctk.CTkButton(app, text="Kliknij mnie")
btn.pack(pady=20)

style = ttk.Style(app)

for style in style.theme_names():
    print(style)
