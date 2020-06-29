import tkinter as tk
from storeData import plotCR

def importData(file):
    root = tk.Tk()
    root.title("Documentation")
    root.geometry("400x200")                      #GUI-dimension

    var = 'X'

    root.grid_columnconfigure((0, 1), weight=1)      #grid creation

    L1 = tk.Label(root, text="Datum")
    L2 = tk.Label(root, text="Probe")
    L3 = tk.Label(root, text="GDL")
    L4 = tk.Label(root, text="Messmethode")

    E1 = tk.Entry(root, width = 40, bd =5)        #enables text string (oneliner) input
    E2 = tk.Entry(root, width = 40, bd =5)
    E3 = tk.Entry(root, width = 40, bd =5)

    B1 = tk.Button(root, text='OK', width= 20, bd=5,command=lambda:[plotCR(file,E1.get(),E2.get(),E3.get(),C1.getvar(var)),root.destroy()])

    C1 = tk.Checkbutton(root, text="mit Messnadel", variable=var, onvalue="m. Nadel", offvalue="o. Nadel")

    L1.grid(row=2, column=0, sticky="w")
    L2.grid(row=3, column=0, sticky="w")
    L3.grid(row=4, column=0, sticky="w")
    L4.grid(row=5, column=0, sticky="w")
    E1.grid(row=2, column=1, sticky="w")
    E2.grid(row=3, column=1, sticky="w")
    E3.grid(row=4, column=1, sticky="w")

    B1.grid(row=6, columnspan=2)
    C1.grid(row=5, column=1)

    root.mainloop()#halts python app for duration of gui