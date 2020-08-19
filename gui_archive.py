import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib

from plot_data import plot_data
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#plot data for archive canvas
def plotter2(dropdown_var, df, canvas):
    df_data = df[df['measurement_spec'] == dropdown_var]
    df_data.sort_values(by=['pressure_rounded[bar]'], inplace=True)
    df_x = df_data['pressure_rounded[bar]']
    df_y_mean = df_data['resistance_mean[mOhm*cm2]']
    df_y_scatter = df_data['resistance[mOhm*cm2]']
    #df_y = [rmean for rmean in df_data['Contact Resistance / mOhm*cm²'] ]

    ax.scatter(df_x, df_y_scatter, label=dropdown_var)
    ax.plot(df_x, df_y_mean)
    canvas.draw()

archive = tk.Tk()
archive.title('Archive')
archive.geometry('1000x1000')
archive.grid_columnconfigure((0, 0), weight=1)

#set startvalue and define optionmenu
var = tk.StringVar(archive)
var.set(measurement_name[0])
option = tk.OptionMenu(archive, var, *measurement_name,
                       command=lambda _: plotter2(var.get(), df_lib,
                                                  plot_canvas))
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
