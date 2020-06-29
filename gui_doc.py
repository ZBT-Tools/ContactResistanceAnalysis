import tkinter as tk
from store_data import store_library


def import_data(file):
    root = tk.Tk()
    root.title("Documentation")
    root.geometry("400x200")                      #GUI-dimension

    var = 'X'

    root.grid_columnconfigure((0, 1), weight=1)      #grid creation

    label1 = tk.Label(root, text="Datum")
    label2 = tk.Label(root, text="Probe")
    label3 = tk.Label(root, text="GDL")
    label4 = tk.Label(root, text="Messmethode")

    entry1 = tk.Entry(root, width=40, bd=5)        #enables text string (oneliner) input
    entry2 = tk.Entry(root, width=40, bd=5)
    entry3 = tk.Entry(root, width=40, bd=5)

    button1 = \
        tk.Button(root, text='OK', width=20, bd=5,
                  command=lambda: [store_library(file, entry1.get(), entry2.get(),
                                                 entry3.get(),
                                                 checkbutton.getvar(var)),
                                   root.destroy()])

    checkbutton = tk.Checkbutton(root, text="mit Messnadel", variable=var,
                                 onvalue="m. Nadel", offvalue="o. Nadel")

    label1.grid(row=2, column=0, sticky="w")
    label2.grid(row=3, column=0, sticky="w")
    label3.grid(row=4, column=0, sticky="w")
    label4.grid(row=5, column=0, sticky="w")
    entry1.grid(row=2, column=1, sticky="w")
    entry2.grid(row=3, column=1, sticky="w")
    entry3.grid(row=4, column=1, sticky="w")

    button1.grid(row=6, columnspan=2)
    checkbutton.grid(row=5, column=1)

    root.mainloop() # halts python app for duration of gui