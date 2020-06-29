import tkinter as tk
from filedialog import get_file

menu = tk.Tk()
menu.title("Menu")
menu.geometry("800x800")

menu.grid_columnconfigure((0, 1), weight=1)

button1 = tk.Button(menu, text='Import new Measurement', width=40, bd=5,
                    command=get_file)
button2 = tk.Button(menu, text='Open Archive', width=40, bd=5)

button1.grid(row=1, columnspan=2)
button2.grid(row=2, columnspan=2)

menu.mainloop()
