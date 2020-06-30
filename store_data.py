import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox
import csv


def store_library(file, date, sample, gdl, spec):

    # Einlesen der Daten in Dataframe
    df_input = pd.read_csv(file, sep='\t', decimal=',', encoding='cp1252',
                           error_bad_lines=False)
    # Separieren der ersten Messreihe in eigenes Dataframe
    df_input = df_input[df_input['I_Ist / mA'] != 0]

    # Ermitteln der Druckmessreihe
    # Drücke auf ganze Zahlen runden und in seperates Dataframe einfügen

    pressure_rounded = df_input['p_Probe_Ist / bar'].round(decimals=0)
    ampere_rounded = (df_input['I_Ist / mA']/1000).round(decimals=1)

    # Name der Kommentarspalte
    commentary_name = 'Kommentar'
    # Name der Messung
    measurement_name = 'Messung'
    # Drücke runden und an das eingelesene Dataframe anhängen
    pressure_rounded = df_input['p_Probe_Ist / bar'].round(decimals=0)
    pressure_rounded_name = 'p_Probe_Ist_rounded / bar'
    df_input.insert(len(df_input.columns), column=pressure_rounded_name,
                    value=pressure_rounded)

    # Ermitteln der einzigartigen Drücke --> Druckmessreihe

    measurements = np.unique(df_input[commentary_name].to_numpy())
    pressures = np.unique(pressure_rounded.to_numpy(dtype=int))
    file_identifier = date + ' ' + sample + ' ' + gdl + ' ' + spec

    df_list = []
    # Für jeden Druck (5 Zyklen / 4 Ströme) werden die jeweiligen Widerstände
    # gemittelt und an die Listen übergeben
    for m in measurements:
        df_t1 = df_input[df_input[commentary_name] == m]
        measurement_identifier = file_identifier + ' ' + m
        df_t1.insert(1, measurement_name, measurement_identifier, True)
        cr_name = 'Contact Resistance / mOhm*cm²'
        cr_mean = 'Contact Resistance / mOhm*cm² - gemittelt'
        df_t1.insert(len(df_t1.columns), cr_name, 0.0, True)
        cr_error_name = 'Contact Resistance Error / mOhm*cm²'
        df_t1.insert(len(df_t1.columns), cr_error_name, 0.0)

        # Deklarieren der benötigten Listen für die Darstellung
        # im Diagramm (y-Achse)
        resistance_mean = []
        resistance_error = []
        for p in pressures:
            df_t2 = df_t1[df_t1[pressure_rounded_name] == p]
            res_g = (df_t2['U_ges-Th_U'] / df_t2['I_Ist / mA']) \
                * 1000.0 * df_t2['Anpressfläche / cm²']

            # Hier muss res_g noch mittels korrekturfaktor anhand des
            # GDL-Alters angepasst werden!

            res_cr = (res_g - df_t2['R_bulk / mOhm*cm²']) / 2.0
            res_cr_mean = res_cr.mean()
            res_cr_error = res_cr.sem()
            df_t1.loc[df_t1[pressure_rounded_name] == p, cr_name] = res_cr
            df_t1.loc[df_t1[pressure_rounded_name] == p, cr_error_name] = \
                res_cr_error
            resistance_mean.append(res_cr_mean)
            resistance_error.append(res_cr_error)

            df_t1.loc[df_t1[pressure_rounded_name] == p, cr_mean] = res_cr_mean

        resistance_mean = np.asarray(resistance_mean)
        resistance_error = np.asarray(resistance_error)
        plt.errorbar(pressures, resistance_mean, yerr=resistance_error,
                     elinewidth=None, capsize=2, label=m)
        df_list.append(df_t1)
    df_result = pd.concat(df_list)
    library_name = 'cr_library.csv'
    if os.path.isfile(library_name):
        with open(library_name, newline='') as file:
            if file.read().find(file_identifier) == -1:
                df_result.to_csv(library_name, mode='a', header=False, sep='\t')
            else:
                tk.messagebox.showinfo(title='Redundanz',
                                       message='Datei bereits im Archiv')
    else:
        df_result.to_csv(library_name, mode='w', header=True, sep='\t')

    # Formatiere Plot
    table_data = [
      ["Date", date],
      ["Sample", sample],
      ["GDL", gdl],
      ["Method", spec]
    ]

    table = plt.table(cellText=table_data, colWidths=[.2, .5], loc='bottom',
                      bbox=[0.49, 0.5, 0.5, 0.2])

    for (row, col), cell in table.get_celld().items():
        if col == 0:
            cell.set_height(1.3)
            cell._loc = 'left'
            cell.set_text_props(ma='left', color='b', fontweight=50)
        elif col == 1:
            cell.set_height(1.3)
            cell._loc = 'right'
            cell.set_text_props(ma='right')

    plt.xlabel('Contact Pressure / bar')
    plt.ylabel('Contact Resistance / mOhm*cm²')
    plt.title('Contact Resistance')
    plt.legend()
    plt.show()





