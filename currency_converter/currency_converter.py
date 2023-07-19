import tkinter as tk
from forex_python.converter import CurrencyRates

c = CurrencyRates()


window = tk.Tk()
window.title("Currency Converter")
window.resizable(width=False, height=False)

frame = tk.Frame(master=window)

entry_currency = tk.Entry(master=frame, width=20)
entry_currency.grid(row=2, column=0, sticky="e")


label_currency = tk.Label(master=frame, text="EUR")
label_currency.grid(row=1, column=3, sticky="w")

label_currency2 = tk.Label(master=frame, text="USD")
label_currency2.grid(row=2, column=3, sticky="w")

label_currency3 = tk.Label(master=frame, text="GBP")
label_currency3.grid(row=3, column=3, sticky="w")

# label_result = tk.Label(master=frame, text="RON")
# label_result.grid(row=3, column=1, padx=10)

frame.grid(row=1, column=1, padx=10)

button = tk.Button(
    master=frame,
    text="RON\N{RIGHTWARDS BLACK ARROW}"
)
button.grid(row=2, column=1, pady=10)

frame.grid(row = 0, column= 0)


window.mainloop()