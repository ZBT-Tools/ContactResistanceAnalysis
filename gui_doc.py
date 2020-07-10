import tkinter as tk
from store_data import store_library


def import_data(file):
    root = tk.Tk()
    root.title("Documentation")
    root.geometry("400x200")                      #GUI-dimension

    var = 'X'
    var2 = 'Y'
    var3 = 'X'
    var4 = 'Y'

    root.grid_columnconfigure((0, 1), weight=1)      #grid creation

    #label1 = tk.Label(root, text="Datum")
    label2 = tk.Label(root, text="Probe")
    label3 = tk.Label(root, text="GDL")
    label4 = tk.Label(root, text="Messmethode")
    label5 = tk.Label(root, text= file)

    #entry1 = tk.Entry(root, width=40, bd=5)        #enables text string (oneliner) input
    entry2 = tk.Entry(root, width=40, bd=5)
    #entry3 = tk.Entry(root, width=40, bd=5)

    button1 = \
        tk.Button(root, text='OK', width=20, bd=5,
                  command=lambda: [store_library(file,
                                    entry2.get(),
                                    checkbutton3.getvar(var3),
                                    checkbutton4.getvar(var4),
                                    checkbutton1.getvar(var),
                                    checkbutton2.getvar(var2)),
                                   root.destroy()])

    checkbutton1 = tk.Checkbutton(root, text="mit Messnadel", variable=var,
                                 onvalue="m. Nadel", offvalue="o. Nadel")

    checkbutton2 = tk.Checkbutton(root, text="Referenz", variable=var2,
                                 onvalue='Referenz', offvalue='')

    checkbutton3 = tk.Checkbutton(root, text="F-H23", variable=var3,
                                  onvalue='H23', offvalue='')

    checkbutton4 = tk.Checkbutton(root, text="SGL-29BC", variable=var4,
                                  onvalue='29BC', offvalue='')

    #label1.grid(row=2, column=0, sticky="w")
    label2.grid(row=3, column=0, sticky="w")
    label3.grid(row=4, column=0, sticky="w")
    label4.grid(row=5, column=0, sticky="w")
    label5.grid(row=8, column=1)

    #entry1.grid(row=2, column=1, sticky="w")
    entry2.grid(row=3, column=1, sticky="w")
    #entry3.grid(row=4, column=1, sticky="w")

    button1.grid(row=7, columnspan=2)

    checkbutton1.grid(row=5, column=1)
    checkbutton2.grid(row=6, column=1)
    checkbutton3.grid(row=4, column=1)
    checkbutton4.grid(row=4, column=2)

    root.mainloop() # halts python app for duration of gui