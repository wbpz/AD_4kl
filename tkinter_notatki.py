import tkinter as tk

root = tk.Tk()
root.title("Edytor notatek")
root.geometry("600x450")

def on_editable_change():
    if radio_button_group.get() == "edit":
        text.config(state=tk.NORMAL)
    else:
        text.config(state=tk.DISABLED)

text = tk.Text(root)
text.pack()
radio_button_group = tk.StringVar(value="edit")
rb_edit = tk.Radiobutton(root, text="Edytowalny", variable=radio_button_group, value="edit", command=on_editable_change)
rb_noedit = tk.Radiobutton(root, text="Nie edytowalny", variable=radio_button_group, value="noedit", command=on_editable_change)
rb_edit.pack(side=tk.LEFT)  
rb_noedit.pack(side=tk.LEFT)



root.mainloop()
    