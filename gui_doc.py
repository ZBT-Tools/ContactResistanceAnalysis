import tkinter as tk
from tkinter import Frame
from store_data import store_library


def import_data(file):
    docu = tk.Tk()
    docu.title("Documentation")
    docu.geometry("{}x{}".format(500, 300))
    docu.maxsize(500, 300)
    docu.config(bg="lightgrey")


    top = Frame(docu, bg='lightgrey', width=500, height=275)
    top.grid_propagate(0)
    bot = Frame(docu, bg='grey', width=500, height=25)
    bot.grid_propagate(0)

    docu.grid_rowconfigure(0, weight=1)
    docu.grid_rowconfigure(1, weight=1)

    top.grid(row=0)
    bot.grid(row=1)

    top.grid_rowconfigure(1, weight=1)
    top.grid_rowconfigure(7, weight=1)
    top.grid_rowconfigure(1, weight=1)
    top.grid_columnconfigure(0, minsize=100, weight=1)
    top.grid_columnconfigure(1, minsize=100, weight=1)
    top.grid_columnconfigure(2, minsize=100, weight=1)

    bot.grid_rowconfigure(1, minsize=25, weight=1)
    top.grid_columnconfigure(0, minsize=100, weight=1)
    top.grid_columnconfigure(1, minsize=100, weight=1)
    top.grid_columnconfigure(2, minsize=100, weight=1)

    var = 'spec'
    var2 = 'ref'
    var3 = 'h23'
    var4 = '29bc'


    #label1 = tk.Label(docu, text="Datum")

    label2 = tk.Label(top, pady=10, text="Sample:", bg='lightgrey')
    label3 = tk.Label(top, pady=10, text="GDL:", bg='lightgrey')
    label4 = tk.Label(top, pady=10, text="Method:", bg='lightgrey')
    label5 = tk.Label(bot, text='Selection: ' + file, bg='grey')


    #entry1 = tk.Entry(docu, width=40, bd=5)        #enables text string (oneliner) input

    entry2 = tk.Entry(top, width=30, bd=5)

    #entry3 = tk.Entry(docu, width=40, bd=5)


    button1 = \
        tk.Button(top, text='OK', width=20, bd=5,
                  command=lambda: [store_library(file,
                                    entry2.get(),
                                    checkbutton3.getvar(var3),
                                    checkbutton4.getvar(var4),
                                    checkbutton1.getvar(var),
                                    checkbutton2.getvar(var2)),
                                   docu.destroy()])

    checkbutton1 = tk.Checkbutton(top, text="Messnadel", variable=var,
                                 onvalue="m. Nadel", offvalue="o. Nadel", bg='lightgrey')

    checkbutton2 = tk.Checkbutton(top, text="Referenz", variable=var2,
                                 onvalue='Referenz', offvalue='', bg='lightgrey')

    checkbutton3 = tk.Checkbutton(top, text="F-H23", variable=var3,
                                  onvalue='H23', offvalue='', bg='lightgrey')

    checkbutton4 = tk.Checkbutton(top, text="SGL-29BC", variable=var4,
                                  onvalue='29BC', offvalue='', bg='lightgrey')


    #label1.grid(row=2, column=0, sticky="w")
    label2.grid(row=2, column=0, padx=20, sticky="w")
    label3.grid(row=3, column=0, padx=20, sticky="w")
    label4.grid(row=4, column=0, padx=20, sticky="w")
    label5.grid(row=0, column=0, columnspan=3, sticky='w')
    label5.config(font=("Courier", 7))

    #entry1.grid(row=2, column=1, sticky="w")

    entry2.grid(row=2, column=1)

    #entry3.grid(row=4, column=1, sticky="w")

    button1.grid(row=6, column=1)

    checkbutton1.grid(row=4, padx= 20, column=1, sticky='w')
    checkbutton2.grid(row=2, padx= 20, column=2, sticky='w')
    checkbutton3.grid(row=3, padx= 20, column=1, sticky='w')
    checkbutton4.grid(row=3, padx= 20, column=2, sticky='w')



    docu.mainloop() # halts python app for duration of gui