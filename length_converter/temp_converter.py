import tkinter as tk

def convert(inch):
    return inch * 2.54

def process_cmd(input_cmp, output_cmp, f):
    input_value = float(input_cmp.get())
    output_value = f(input_value)
    output_cmp["text"] = f"{output_value} CM"



window = tk.Tk()
window.title("Length Converter")
window.resizable(width=False, height=False)

frm_entry = tk.Frame(master=window)
entry_temperature = tk.Entry(master=frm_entry, width=10)
label_temperature = tk.Label(master=frm_entry, text="INCH")

entry_temperature.grid(row=0, column=0, sticky="e")
label_temperature.grid(row=0, column=1, sticky="w")

btn_convert = tk.Button(
    master=window,
    text="\N{RIGHTWARDS BLACK ARROW}",
    command=lambda : process_cmd(entry_temperature, lbl_result, convert)
)
lbl_result = tk.Label(master=window, text="CM")


frm_entry.grid(row=0, column=0, padx=10)
btn_convert.grid(row=0, column=1, pady=10)
lbl_result.grid(row=0, column=2, padx=10)



window.mainloop()