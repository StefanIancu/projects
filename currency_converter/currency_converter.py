import tkinter as tk
from forex_python.converter import CurrencyRates
from datetime import datetime
import geocoder

c = CurrencyRates()

now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

my_location = geocoder.ip("me")
location = str(my_location[::-1]).strip("[]")


def convert_to_eur(ron:float):
    to_eur = c.convert("RON", "EUR", ron)
    to_usd = c.convert("RON", "USD", ron)
    to_gbp = c.convert("RON", "GBP", ron)
    return [round(to_eur, 2), round(to_usd, 2), round(to_gbp, 2)]

def process_command(input_cmp, output_cmp, outcmp2, outcmp3, f):
    input_value = float(input_cmp.get())
    output_value = f(input_value)
    output_cmp["text"] = f"{output_value[0]} EUR"
    outcmp2["text"] = f"{output_value[1]} USD"
    outcmp3["text"] = f"{output_value[2]} GBP"


window = tk.Tk()
window.title("Currency Converter")
window.resizable(width=False, height=False)

frame = tk.Frame(master=window)

entry_currency = tk.Entry(master=frame, width=20)
entry_currency.grid(row=2, column=0, sticky="e")

date_today = tk.Label(master=frame, text=f"{formatted_time}")
date_today.grid(row=1, column=0, sticky="w")

user_location = tk.Label(master=frame, text=f"{location}")
user_location.grid(row=3, column=0, sticky="w")

label_currency = tk.Label(master=frame, text="EUR")
label_currency.grid(row=1, column=3, sticky="w")

label_currency2 = tk.Label(master=frame, text="USD")
label_currency2.grid(row=2, column=3, sticky="w")

label_currency3 = tk.Label(master=frame, text="GBP")
label_currency3.grid(row=3, column=3, sticky="w")

frame.grid(row=1, column=1, padx=10)
frame.grid(row = 0, column= 0)

button = tk.Button(
    master=frame,
    text="RON\N{RIGHTWARDS BLACK ARROW}",
    command= lambda : process_command(entry_currency, label_currency, label_currency2, label_currency3, convert_to_eur),
)
button.grid(row=2, column=1, pady=10)



window.mainloop()