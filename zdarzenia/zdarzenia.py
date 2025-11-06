import tkinter as tk

root = tk.Tk()
root.title("Zdarzenia   ")
root.geometry("600x450")

label = tk.Label(root, text="SYSTEM ROZBROJONY", fg="white", bg="green", padx=10, pady=10)
label.place(relx=0.5, rely=0.5, anchor="center")

label.bind("<Enter>", lambda e: label.config(bg="yellow", text="UZBROJENIE MOŻLIWE", fg="black"))
label.bind("<Leave>", lambda e: label.config(bg="green", fg="white", text="SYSTEM ROZBROJONY"))
label.bind("<Button-1>", lambda e: label.config(bg="red", fg="white", text="SYSTEM UZBROJONY!"))


root.mainloop()
    