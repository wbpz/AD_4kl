import json, requests, threading, customtkinter as ctk, tkinter.ttk as ttk

TARGET_URL = "http://api.nbp.pl/api/exchangerates/tables/A/?format=json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("api")

def get_rates():
	request = requests.get(TARGET_URL)
	content = json.loads(request.content)
	assert len(content) == 1
	content = content[0]
	print(content)
	rates = content["rates"]
	return rates, content["effectiveDate"]

def calculate():
    try:
        rates, date = get_rates()
        num = int(pln.get())
        target = [rate for rate in rates if rate["code"] == options.get()][0]
        result.configure(text=f"Wartość to {round(num/target["mid"] * 100) / 100} {options.get()}\n{date}")
    except Exception as e:
        result.configure(text=f"Błąd: \"{str(e)}\"")


pln = ctk.CTkEntry(app)
pln.pack(pady=10)

rates, _ = get_rates()

options = ctk.CTkOptionMenu(app, values=[rate["code"] for rate in rates])
options.pack(pady=10)
	
options.set("USD")

btn = ctk.CTkButton(app, text="Request", command=lambda: threading.Thread(target=calculate).start())
btn.pack(pady=10)

result = ctk.CTkLabel(app, text="")
result.pack(pady=10)

app.mainloop()
