import tkinter as tk
from filedialog import get_file
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec
from matplotlib.figure import Figure
import numpy as np
from tkinter import Frame
from tkinter import PhotoImage
from PIL import ImageTk, Image
import glob

from plot_data import plot_data
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plotter2(dropdown_var, df, canvas, subf1, subf2):
    df_data = df[df['measurement'] == dropdown_var]
    meas = np.unique(df_data['measurement'].to_numpy())
    df_data.sort_values(by=['pressure_rounded[bar]'], inplace=True)
    df_pressure = df_data['pressure_rounded[bar]']
    pressures = np.unique(df_data['pressure_rounded[bar]'].to_numpy(dtype=int))

    df_res_mean = []
    df_contact_res_mean = []
    df_volume_res_mean = []
    df_bulk_res_mean = []

    for p in pressures:

        df_data2 = df_data[df_data['pressure_rounded[bar]'] == p]
        res_plot = df_data2['resistance_mean[mOhm*cm2]']
        contact_res_plot = df_data2['contact_resistance_mean[mOhm*cm2]']
        volume_res_plot = df_data2['volume_resistance_mean[mOhm*cm2]']
        bulk_res_plot = df_data2['bulk_resistance_mean[mOhm*cm2]']

        res_mean_plot = res_plot.mean()
        contact_res_mean_plot = contact_res_plot.mean()
        volume_res_mean_plot = volume_res_plot.mean()
        bulk_res_mean_plot = bulk_res_plot.mean()

        df_res_mean.append(res_mean_plot)
        df_contact_res_mean.append(contact_res_mean_plot)
        df_volume_res_mean.append(volume_res_mean_plot)
        df_bulk_res_mean.append(bulk_res_mean_plot)


    #df_res_mean = df_data['resistance_mean[mOhm*cm2]']
    df_contact_res = df_data['contact_resistance_mean[mOhm*cm2]']
    df_res = df_data['resistance_mean[mOhm*cm2]']
    #df_y = [rmean for rmean in df_data['Contact Resistance / mOhm*cm²'] ]

    #subf.scatter(df_pressure, df_res, label=dropdown_var)
    #subf.plot(df_pressure, df_res_mean)

    #subf.plot(pressures, df_res_mean, label=meas)
    #subf.plot(pressures, df_contact_res_mean, label='Contact Resistance')
    #subf.plot(pressures, df_volume_res_mean, label='Volume Resistance')
    #subf.plot(pressures, df_bulk_res_mean, label='Bulk Resistance')

    subf1.plot(pressures, df_contact_res_mean, linestyle='dashed', linewidth=3, marker='s', markersize=12,  label=meas)
    subf2.bar(pressures, df_contact_res_mean, tick_label=meas, width=0.8, color =['red', 'green'])
    #subf.title('SGL 29BC')
    subf1.legend(loc='upper right')
    canvas.draw()



def create_archive():
    archive = tk.Toplevel()
    archive.title('Archive')
    archive.geometry('2000x1000')
    archive.grid_columnconfigure((0, 0), weight=1)

    #read library and get names of measurements
    df_lib = pd.read_csv('cr_library.csv')
    measurement_name = df_lib['measurement'].unique()

    #set startvalue and define optionmenu
    var = tk.StringVar(archive)
    var.set(measurement_name[0])
    option = tk.OptionMenu(archive, var, *measurement_name,
                           command=lambda _: plotter2(var.get(), df_lib,
                                                      plot_canvas, fig_ax1, fig_ax2))
    option.pack()



    font = {'family': 'arial',
            'color': 'black',
            'weight': 'normal',
            'size': 16}

    fig = Figure(figsize=(50, 50))
    grid = fig.add_gridspec(10,10)

    fig_ax1 = fig.add_subplot(grid[:10, :-4])
    fig_ax1.set_title('Contact Resistance')
    fig_ax1.set_xlim([0, 21])
    fig_ax1.set_ylim([0, 50])

    fig_ax2 = fig.add_subplot(grid[:5, 6:])
    fig_ax2.set_title('CR @ 20bar')

    fig_ax3 = fig.add_subplot(grid[1:3, 3:5])
    fig_ax3.set_title('Test')

    #fig, ax1 = plt.subplots(gridspec_kw=grid)
    #ax1.text(0.5, 0.5, 'Axes 1', ha='center', va='center', size=24, alpha=.5)

    # ax2 = plt.subplot(grid[0, 1])
    #ax2.set_xticks(())
    #ax2.set_yticks(())
    #ax2.text(0.5, 0.5, 'Axes 2', ha='center', va='center', size=24, alpha=.5)


    # fig, ax = plt.subplots(1, 2, figsize=(100, 100))
    #
    # ax[0].set_xlabel('Contact Pressure / bar', fontdict=font, fontsize=14, labelpad=20)
    # ax[0].set_ylabel('Contact Resistance / mOhm*cm²', fontdict=font, fontsize=14, labelpad=20)
    # ax[0].set_title('Contact Resistance', fontdict=font, fontsize=16, pad=10)
    # ax[0].set_xlim([0, 25])
    # ax[0].set_ylim([0, 50])
    # #ax[0].legend(loc="upper right")
    #
    # ax[1].set_xlabel('Contact Pressure / bar', fontdict=font, fontsize=14, labelpad=20)
    # ax[1].set_ylabel('Contact Resistance / mOhm*cm²', fontdict=font, fontsize=14, labelpad=20)
    # ax[1].set_title('Contact Resistance', fontdict=font, fontsize=16, pad=10)
    # ax[1].set_xlim([0, 25])
    # ax[1].set_ylim([0, 50])
    #ax[1].legend(loc="upper right")



    plot_canvas = FigureCanvasTkAgg(fig, master=archive)
    plot_canvas.get_tk_widget().pack()

    archive.mainloop()

menu = tk.Tk()
menu.title("Contact Resistance Analysis")
menu.geometry("{}x{}".format(500, 350))
menu.maxsize(500, 350)
menu.config(bg='lightgrey')

top = Frame(menu, bg='lightgrey', width=500, height=100)
top.grid_propagate(0)
center = Frame(menu, bg='grey', width=500, height=250)
center.grid_propagate(0)

menu.grid_rowconfigure(0, weight=1)
menu.grid_rowconfigure(1, weight=1)

top.grid(row=0)
center.grid(row=1)

#top.grid_rowconfigure(0, weight=1)
#top.grid_rowconfigure(1, weight=1)
#top.grid_columnconfigure(0, minsize=50, weight=1)
#top.grid_columnconfigure(1, minsize=50, weight=1)

button1 = tk.Button(top, text='Import new Measurement', width=40,
                    command=get_file)

button2 = tk.Button(top, text='Analyze Data', width=40,
                    command=lambda:create_archive())

im_cr = Image.open('cr_test.png')
im_zbt = Image.open('zbt.png')

ph_cr = ImageTk.PhotoImage(im_cr.resize((200, 200), Image.ANTIALIAS))
ph_zbt = ImageTk.PhotoImage(im_zbt.resize((100, 50), Image.ANTIALIAS))

label_ph_cr = tk.Label(center, image=ph_cr, width=200, height=200)
label_ph_zbt = tk.Label(top, image=ph_zbt, width=100, height=50)

button1.grid(padx=(20, 0), pady=10, row=0, column=0, sticky='w')
button2.grid(padx=(20, 0), pady=10, row=1, column=0, sticky='w')

label_ph_cr.grid(padx=150, pady=10)
label_ph_zbt.grid(padx=85, row=0, column=1, sticky='ne')

menu.mainloop()

#plot data for archive canvas

