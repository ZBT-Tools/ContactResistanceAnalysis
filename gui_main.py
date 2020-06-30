import tkinter as tk
from filedialog import get_file
import pandas as pd
import matplotlib
from matplotlib.figure import Figure

from plot_data import plot_data
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plotter2(dropdown_var, df, canvas, subf):
    df_data = df[df['Messung'] == dropdown_var]
    df_data.sort_values(by=['p_Probe_Ist_rounded / bar'], inplace=True)
    df_x = df_data['p_Probe_Ist_rounded / bar']
    df_y_mean = df_data['Contact Resistance / mOhm*cm² - gemittelt']
    df_y_scatter = df_data['Contact Resistance / mOhm*cm²']
    #df_y = [rmean for rmean in df_data['Contact Resistance / mOhm*cm²'] ]

    subf.scatter(df_x, df_y_scatter, label=dropdown_var)
    subf.plot(df_x, df_y_mean)
    canvas.draw()

def create_archive():
    archive = tk.Toplevel()
    archive.title('Archive')
    archive.geometry('1000x1000')
    archive.grid_columnconfigure((0, 0), weight=1)

    #read library and get names of measurements
    df_lib = pd.read_csv('cr_library.csv', sep='\t')
    measurement_name = df_lib['Messung'].unique()

    #set startvalue and define optionmenu
    var = tk.StringVar(archive)
    var.set(measurement_name[0])
    option = tk.OptionMenu(archive, var, *measurement_name,
                           command=lambda _: plotter2(var.get(), df_lib,
                                                      plot_canvas, ax))
    option.pack()

    fig = Figure(figsize=(50, 50))
    ax = fig.add_subplot()

    ax.set_xlabel('Contact Pressure / bar')
    ax.set_ylabel('Contact Resistance / mOhm*cm²')
    ax.set_title('Contact Resistance', fontsize=16)
    ax.legend(loc="upper right")

    plot_canvas = FigureCanvasTkAgg(fig, master=archive)
    plot_canvas.get_tk_widget().pack()

    archive.mainloop()


menu = tk.Tk()
menu.title("Menu")
menu.geometry("800x800")

menu.grid_columnconfigure((0, 1), weight=1)

button1 = tk.Button(menu, text='Import new Measurement', width=40, bd=5,
                    command=get_file)
button2 = tk.Button(menu, text='Open Archive', width=40, bd=5, command=lambda:create_archive())

button1.grid(row=1, columnspan=2)
button2.grid(row=2, columnspan=2)

menu.mainloop()

#plot data for archive canvas

