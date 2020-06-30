import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox


def store_library(file, date, sample, gdl, spec):
    #einlesen der Daten in Dataframe --> df_compl
    df_compl = pd.read_csv(file, sep='\t', decimal=',', encoding='cp1252',
                         error_bad_lines=False)

    #separieren der ersten Messreihe in eigens Dataframe --> df_m1
    df_compl = df_compl[df_compl['I_Ist / mA'] != 0]

    # Ermitteln der Druckmessreihe
    # Drücke auf ganze Zahlen runden und in seperates Dataframe einfügen

    pressure_rounded = df_compl['p_Probe_Ist / bar'].round(decimals=0)

    # Umebennenung der Druckspalte mit gerundeten Werten

    pressure_rounded_name = 'p_Probe_Ist_rounded / bar'
    measurement_split = 'Kommentar'

    # Spalte mit gerundetem Druck wird an die letzte Spalte des Dataframes der Messung I angefügt

    df_compl.insert(len(df_compl.columns), column=pressure_rounded_name,
                    value=pressure_rounded)

    # Ermitteln der einzigartigen Drücke --> Druckmessreihe

    measurements = np.unique(df_compl['Kommentar'].to_numpy())
    pressures = np.unique(pressure_rounded.to_numpy(dtype=int))

    # Für jeden Druck (5 Zyklen / 4 Ströme) werden die jeweiligen Widerstände gemittelt und an die Listen übergeben
    for m in measurements:
        df_t1 = df_compl[df_compl['Kommentar'] == m]
        samplespec = date + ' ' + sample + ' ' + gdl + ' ' + spec + ' ' + m
        df_t1.insert(1, 'Messung', samplespec, True)
        cr_name = 'Contact Resistance / mOhm*cm²'
        df_t1.insert(len(df_t1.columns), cr_name, 0.0, True)
        cr_error_name = 'Contact Resistance Error / mOhm*cm²'
        df_t1.insert(len(df_t1.columns), cr_error_name, 0.0)

        # Deklarieren der benötigten Listen für die Darstellung im Diagramm (y-Achse)
        resistance_mean = []
        resistance_error = []
        for p in pressures:
            df_t2 = df_t1[df_t1[pressure_rounded_name] == p]
            res_g = (df_t2['U_ges-Th_U'] / df_t2['I_Ist / mA']) \
                * 1000.0 * df_t2['Anpressfläche / cm²']

            #hier muss res_g noch mittels korrekturfaktor an Hand des GDL alters angepasst werden!

            res_cr = (res_g - df_t2['R_bulk / mOhm*cm²']) / 2.0
            res_cr_mean = res_cr.mean()
            res_cr_error = res_cr.sem()
            df_t1.loc[df_t1[pressure_rounded_name] == p, cr_name] = res_cr
            df_t1.loc[df_t1[pressure_rounded_name] == p, cr_error_name] = \
                res_cr_error
            resistance_mean.append(res_cr_mean)
            resistance_error.append(res_cr_error)
        resistance_mean = np.asarray(resistance_mean)
        resistance_error = np.asarray(resistance_error)
        plt.errorbar(pressures, resistance_mean, yerr=resistance_error,
                     elinewidth=None, capsize=2, label=m)

        # df_t1.insert(len(df_t1.columns), 'Contact Resistance / mOhm*cm²',
        #              resistance_mean, True)
        # df_t1.insert(len(df_t1.columns),
        #              'Contact Resistance Error / mOhm*cm²', resistance_error)

        library_name = "cr_library.csv"
        if os.path.isfile(library_name):
            if open(library_name, 'r').read().find(samplespec) == -1:
                df_t1.to_csv(library_name, mode='a', header=False, sep='\t')
            else:
                tk.messagebox.showinfo(title='Redundanz',
                                       message='Messung bereits im Archiv')
        else:
            df_t1.to_csv(library_name, mode='w', header=True, sep='\t')
    # rowLabels = ['Date', 'Sample', 'GDL', 'Method']
    # cellText = [date, sample, gdl, spec]
    # plt.table(cellText=cellText, rowLoc='right', rowLabels=rowLabels, colWidths=[.5,.5], colLoc='center', loc='bottom', bbox = [0.1, 0, 0.9, 0.8])

    # description = 'Datum:   '+date+'\nGDL:    '+gdl+'\nProbe:   '+sample+'\nMethode:    '+spec
    # plt.text(15, 100, description, bbox=dict(facecolor='blue', alpha=0.2), horizontalalignment='left', verticalalignment='center')

    #fig, ax = plt.subplots()

    table_data = [
      ["Date", date],
      ["Sample", sample],
      ["GDL", gdl],
      ["Method", spec]
    ]

    table = plt.table(cellText=table_data, colWidths=[.2, .5], loc='bottom',
                      bbox=[0.49, 0.5, 0.5, 0.2])

    for (row, col), cell in table.get_celld().items():

      if (col == 0):
        cell.set_height(1.3)
        cell._loc = 'left'
        cell.set_text_props(ma='left', color='b', fontweight=50)
      elif (col == 1):
        cell.set_height(1.3)
        cell._loc = 'right'
        cell.set_text_props(ma='right')

    plt.xlabel('Contact Pressure / bar')
    plt.ylabel('Contact Resistance / mOhm*cm²')
    plt.title('Contact Resistance')
    plt.legend()
    plt.show()





