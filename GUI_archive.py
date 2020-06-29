import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

from plotData import plotData
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def plotter():
    fig = Figure(figsize=(50, 50))
    a = fig.add_subplot(111)
    a.scatter(plotData(var.get())[0],plotData(var.get())[1], color='red')
    a.plot(plotData(var.get())[0],plotData(var.get())[1], color='blue')

    a.set_xlabel('Contact Pressure / bar')
    a.set_ylabel('Contact Resistance / mOhm*cm²')
    a.set_title('Contact Resistance', fontsize = 16)

    #graph = plt.errorbar(pressures, resistance_mean, yerr=resistance_error, elinewidth=None, capsize=2, label=meas)

    canvas = FigureCanvasTkAgg(fig, master=archive)
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    #canvas.draw()
    fig.canvas.draw_idle()


archive = tk.Tk()
archive.title('Archive')
archive.geometry('1000x1000')
archive.grid_columnconfigure((0, 1), weight=1)

df_lib = pd.read_csv('cr_library.csv')
df_lib.rename(index={2: "Messung"})
measurement = df_lib['Messung'].unique()


var = tk.StringVar(archive)
var.set(measurement[0]) # initial value

option = tk.OptionMenu(archive, var, *measurement, command=lambda _: plotter())
option.grid(row=2, columnspan=2)

fig = Figure(figsize=(200, 200))
a = fig.add_subplot(111)
a.scatter(plotData(var.get())[0],plotData(var.get())[1], color='red')
a.plot(plotData(var.get())[0],plotData(var.get())[1], color='blue')
plt.plot

a.set_xlabel('Contact Pressure / bar')
a.set_ylabel('Contact Resistance / mOhm*cm²')
a.set_title('Contact Resistance', fontsize = 16)

    #graph = plt.errorbar(pressures, resistance_mean, yerr=resistance_error, elinewidth=None, capsize=2, label=meas)

canvas = FigureCanvasTkAgg(fig, master=archive)
canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
canvas.draw()

# plt.legend()
# plt.show()

archive.mainloop()
