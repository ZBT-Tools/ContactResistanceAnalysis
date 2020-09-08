import tkinter as tk
import pandas as pd
import numpy as np
from tkinter import Frame
import matplotlib.gridspec
from matplotlib.figure import Figure
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

demo = tk.Tk()
demo.title("Test")
demo.geometry("{}x{}".format(1300, 800))
demo.config(bg='lightgrey')

top = Frame(demo, bg='darkblue', width=1300, height=100)
top.grid_propagate(0)
center = Frame(demo, bg='grey', width=1300, height=200)
center.grid_propagate(0)
bot = Frame(demo, bg='lightgrey', width=1300, height=500)
bot.grid_propagate(0)

demo.grid_rowconfigure(0, weight=1)
demo.grid_rowconfigure(1, weight=1)
demo.grid_rowconfigure(2, weight=1)

top.grid(row=0)
center.grid(row=1)
bot.grid(row=2)

entry_1 = tk.Entry(top, width=30, bd=5)

def plotter2(file_name, meas_name, canvas, subf1, subf2, subf3, subf4, subf5):
    print(file_name)
    print(meas_name)
    if file_name == 'pp_messreihe':
        df_file = pd.read_csv('pp_messreihe.csv')
    elif file_name == 'sol_gel_messreihe':
        df_file = pd.read_csv('sol_gel_messreihe.csv')
    else:
        df_file = pd.read_csv('cr_library.csv')

    df_data = df_file[df_file['measurement'] == meas_name]
    #meas = np.unique(df_data['measurement'].to_numpy())
    x = str(meas_name).split()
    bar_name = x[1]
    df_data.sort_values(by=['pressure_rounded[bar]'], inplace=True)
    pressures = np.unique(df_data['pressure_rounded[bar]'].to_numpy(dtype=int))

    df_res_main_as_mean = []
    df_res_flow_as_mean = []
    df_res_bulk_as_mean = []
    df_res_contact_as_mean = []

    df_con_main_vs_mean = []
    df_con_flow_vs_mean = []
    df_con_bulk_vs_mean = []

    for p in pressures:

        df_data2 = df_data[df_data['pressure_rounded[bar]'] == p]

        res_main_as_plot = df_data2['as_main_resistance_mean[mOhm*cm2]']
        res_through_as_plot = df_data2['as_flow_resistance_mean[mOhm*cm2]']
        res_bulk_as_plot = df_data2['as_bulk_resistance_mean[mOhm*cm2]']
        res_contact_as_plot = df_data2['as_contact_resistance_mean[mOhm*cm2]']

        res_main_vs_plot = df_data2['vs_main_resistance_mean[mOhm*cm]']
        res_through_vs_plot = df_data2['vs_flow_resistance_mean[mOhm*cm]']
        res_bulk_vs_plot = df_data2['vs_bulk_resistance_mean[mOhm*cm]']

        con_main_vs_plot = df_data2['vs_main_conductance_mean[S/cm]']
        con_through_vs_plot = df_data2['vs_flow_conductance_mean[S/cm]']
        con_bulk_vs_plot = df_data2['vs_bulk_conductance_mean[S/cm]']

        #flächenspezifische Widerstände
        res_main_as_mean_plot = res_main_as_plot.mean()
        res_through_as_mean_plot = res_through_as_plot.mean()
        res_bulk_as_mean_plot = res_bulk_as_plot.mean()
        res_contact_as_mean_plot = res_contact_as_plot.mean()

        #volumenspezifische Widerstände
        res_main_vs_mean_plot = res_main_vs_plot.mean()
        res_through_vs_mean_plot = res_through_vs_plot.mean()
        res_bulk_vs_mean_plot = res_bulk_vs_plot.mean()

        #Leitwerte
        con_main_vs_mean_plot = con_main_vs_plot.mean()
        con_through_vs_mean_plot = con_through_vs_plot.mean()
        con_bulk_vs_mean_plot = con_bulk_vs_plot.mean()

        if p == 20:
            mr_as_at_20bar = res_main_as_mean_plot
            fr_as_at_20bar = res_through_as_mean_plot
            br_as_at_20bar = res_bulk_as_mean_plot
            cr_as_at_20bar = res_contact_as_mean_plot

            mr_vs_at_20bar = res_main_vs_mean_plot
            fr_vs_at_20bar = res_through_vs_mean_plot
            br_vs_at_20bar = res_bulk_vs_mean_plot

            con_mvs_at_20bar = con_main_vs_mean_plot
            con_fvs_at_20bar = con_through_vs_mean_plot
            con_bvs_at_20bar = con_bulk_vs_mean_plot

        df_res_main_as_mean.append(res_main_as_mean_plot)
        df_res_flow_as_mean.append(res_through_as_mean_plot)
        df_res_bulk_as_mean.append(res_bulk_as_mean_plot)
        df_res_contact_as_mean.append(res_contact_as_mean_plot)


    subf1.plot(pressures, df_res_contact_as_mean, linestyle='dashed', linewidth=2, marker='s', markersize=4, label=meas_name)
    subf1.legend(loc='upper left', bbox_to_anchor=(-0.2, 1.15), ncol=5, fontsize=8)
    subf1.set_ylim([0, 150])

    # subf2.bar(bar_name, cr_as_at_20bar, width=1)
    # subf2.tick_params('x', labelsize=8, labelrotation=90)
    #
    #
    # subf3.bar(bar_name, con_mvs_at_20bar, width=1)
    # subf3.tick_params('x', labelsize=8, labelrotation=90)
    #
    # subf4.bar(bar_name, con_fvs_at_20bar, width=1)
    # subf4.tick_params('x', labelsize=8, labelrotation=90)
    #
    # subf5.bar(bar_name, con_bvs_at_20bar, width=1)
    # subf5.tick_params('x', labelsize=8, labelrotation=90)

    canvas.draw()

list_cb = []
list_var = []
dict_cb_var = {}

def read_data(file):
    list = center.grid_slaves()
    for l in list:
        l.destroy()

    if file == 'pp_messreihe':
        df_meas = pd.read_csv('pp_messreihe.csv')
    elif file == 'sol_gel_messreihe':
        df_meas = pd.read_csv('sol_gel_messreihe.csv')
    else:
        df_meas = pd.read_csv('cr_library.csv')

    measurements = df_meas['measurement'].unique()

    x = 0

    for i, m in enumerate(measurements):

        measurements[i] = tk.StringVar()
        list_var.append(measurements[i])

        cb_name = 'cb_' + str(x)
        list_cb.append(cb_name)

        dict_cb_var[cb_name] = measurements[i]

        # var = tk.StringVar(demo)
        # var.set(m)
        # print(var.get())
        # list_var.append(var)

        cb_name = tk.Checkbutton(center, variable=dict_cb_var[cb_name], text=m,
                                 command=lambda : plotter2(file, dict_cb_var[cb_name],
                                                            plot_canvas, fig_ax1,
                                                            fig_ax2, fig_ax3,
                                                            fig_ax4, fig_ax5))

        if x<5:
            cb_name.grid(row=0, padx=20, pady=10, column=x, sticky='w')
        elif x>=5 and x<10:
            cb_name.grid(row=1, padx=20, pady=10, column=x-5, sticky='w')
        elif x >= 10 and x < 15:
            cb_name.grid(row=2, padx=20, pady=10, column=x-10, sticky='w')
        else:
            cb_name.grid(row=3, padx=20, pady=10, column=x-15, sticky='w')

        list_cb.append(cb_name)

        x += 1

    print(list_cb)
    print(dict_var)

demo_selection = tk.StringVar(demo)
selections = [' ', 'pp_messreihe', 'sol_gel_messreihe', 'c']
demo_selection.set(selections[0])

option_1 = tk.OptionMenu(top, demo_selection, *selections,
                         command=lambda _: read_data(demo_selection.get()))

option_1.grid(row=0, column=0)

fig = Figure(figsize=(50, 50))
grid = fig.add_gridspec(12, 18)

fig_ax1 = fig.add_subplot(grid[:12, :-8])
fig_ax1.set_title('Kontaktwiderstand')
#fig_ax1.set_xlim([0, 21])
#fig_ax1.set_ylim([0, 50])

fig_ax2 = fig.add_subplot(grid[1:6, 5:10])
fig_ax2.set_title('KW @ 20bar')

fig_ax3 = fig.add_subplot(grid[:3, 12:])
fig_ax3.set_title('volumetrischer Gesamt-Leitwert [S/cm]')

fig_ax4 = fig.add_subplot(grid[4:7, 12:])
fig_ax4.set_title('volumetrischer Durchgangs-Leitwert [S/cm]')

fig_ax5 = fig.add_subplot(grid[8:11, 12:])
fig_ax5.set_title('volumetrischer Bulk-Leitwert [S/cm]')

plot_canvas = FigureCanvasTkAgg(fig, master=demo)
#plot_canvas.get_tk_widget().pack()


demo.mainloop()