import tkinter as tk
from filedialog import getFile

menu = tk.Tk()
menu.title("Menu")
menu.geometry("800x800")

menu.grid_columnconfigure((0, 1), weight=1)

B1 = tk.Button(menu, text='Import new Measurement', width= 40, bd=5, command=getFile)
B2 = tk.Button(menu, text='Open Archive', width= 40, bd=5)

B1.grid(row=1, columnspan=2)
B2.grid(row=2, columnspan=2)

menu.mainloop()