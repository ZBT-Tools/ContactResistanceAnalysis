from typing import Optional, Union, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox

from numpy.core._multiarray_umath import ndarray


def store_library(file, date, sample, gdl, spec):

    # read datafile
    df_input = pd.read_csv(file, sep='\t', decimal=',', encoding='cp1252',
                           error_bad_lines=False)

    # clear measurement artefacts
    df_input = df_input[df_input['I_Ist / mA'] != 0]

    # define variable --> commentary_name
    commentary_name = 'Kommentar'
    # define variable --> measurement_name
    measurement_name = 'Messung'

    # round pressures and append to df in seperate column
    pressure_rounded = df_input['p_Probe_Ist / bar'].round(decimals=0)
    pressure_rounded_name = 'p_Probe_Ist_rounded / bar'
    df_input.insert(len(df_input.columns), column=pressure_rounded_name,
                    value=pressure_rounded)

    # seperate measurements by cycles
    df_input['cycle'] = ''
    z = 1
    rec = 0
    for i, v in df_input['p_Probe_Ist_rounded / bar'].items():
        if v >= rec:

            df_input['cycle'].loc[i] = z

            if df_input.loc[v, 'I_Ist / mA'] < 600:
                rec = v
        else:
            z += 1
            rec = 0
            df_input['cycle'].iloc[i] = z

    # get unique values as lists --> measurements / pressures / cycles
    measurements = np.unique(df_input[commentary_name].to_numpy())
    pressures = np.unique(pressure_rounded.to_numpy(dtype=int))
    cycles = np.unique(df_input['cycle'].to_numpy(dtype=int))


    # create variable for storage in library -_> file_identifier
    file_identifier = date + ' ' + sample + ' ' + gdl + ' ' + spec

    # create empty df which will be filled with storage data
    df_list = []

    fig, a = plt.subplots(2, 3)

    # seperate datafile into different measurements
    for m in measurements:

        # df-slice with single measurement
        df_t1 = df_input[df_input[commentary_name] == m]

        # specify file-identifer and add measurement
        measurement_identifier = file_identifier + ' ' + m

        # add measurement_identifer / cr / cr_error / cr_mean to df
        # TODO: rework for structures (those columns can be initalized earlier!)
        df_t1.insert(1, measurement_name, measurement_identifier, True)

        cr_name = 'Contact Resistance / mOhm*cm²'
        df_t1.insert(len(df_t1.columns), cr_name, 0.0, True)

        cr_error_name = 'Contact Resistance Error / mOhm*cm²'
        df_t1.insert(len(df_t1.columns), cr_error_name, 0.0)

        cr_mean = 'Contact Resistance / mOhm*cm² - gemittelt'
        df_t1.insert(len(df_t1.columns), cr_mean, 0.0)

        r_name = 'Gesamtwiderstand / mOhm*cm²'
        df_t1.insert(len(df_t1.columns), r_name, 0.0)

        r_mean = 'Gesamtwiderstand / mOhm*cm² - gemittelt'
        df_t1.insert(len(df_t1.columns), r_mean, 0.0)

        r_error_name = 'Gesamtwiderstand Error/ mOhm*cm²'
        df_t1.insert(len(df_t1.columns), r_error_name, 0.0)

        r_bulk_name= 'Bulk-Widerstand / mOhm*cm²'
        df_t1.insert(len(df_t1.columns), r_bulk_name, 0.0)

        r_bulk_mean = 'Bulk-Widerstand / mOhm*cm² - gemittelt'
        df_t1.insert(len(df_t1.columns), r_bulk_mean, 0.0)

        r_bulk_error = 'Bulk-Widerstand Error/ mOhm*cm²'
        df_t1.insert(len(df_t1.columns), r_bulk_error, 0.0)



        # seperate measurement-df into different cycles
        for c in cycles:

            # df-slice of measurement-df with single cycle
            df_t2_c = df_t1[df_t1['cycle'] == c]

            # declare empty y / y-error-value list for plotting --> contact res
            resistance_mean = []
            resistance_error = []

            resistance_g_mean = []
            resistance_g_error = []

            resistance_bulk_mean = []
            resistance_bulk_error = []

            # seperate cycle-df into different pressures
            for p in pressures:

                # df-slice of cycle-df with single pressure
                df_t3 = df_t2_c[df_t2_c[pressure_rounded_name] == p]

                # calculate --> overall resistance
                res_g = (df_t3['U_ges-Th_U'] / df_t3['I_Ist / mA']) \
                    * 1000.0 * df_t3['Anpressfläche / cm²']

                # TODO: Hier muss res_g noch mittels korrekturfaktor anhand des GDL-Alters angepasst werden!

                res_bulk = df_t3['R_bulk / mOhm*cm²']
                # calculate --> contact resistance
                res_cr = (res_g - df_t3['R_bulk / mOhm*cm²']) / 2.0

                # get mean- and sem-value of calculated resistance
                res_cr_mean = res_cr.mean()
                res_cr_error = res_cr.sem()

                res_g_mean = res_g.mean()
                res_g_error = res_g.sem()

                res_bulk_mean = res_bulk.mean()
                res_bulk_error = res_bulk.sem()

                # write data --> cr-mean and cr-sem in df-slice
                df_t3.loc[df_t3[pressure_rounded_name] == p, cr_name] = res_cr
                df_t3.loc[df_t3[pressure_rounded_name] == p, cr_mean] = res_cr_mean
                df_t3.loc[df_t3[pressure_rounded_name] == p, cr_error_name] = res_cr_error

                df_t3.loc[df_t3[pressure_rounded_name] == p, r_name] = res_g
                df_t3.loc[df_t3[pressure_rounded_name] == p, r_mean] = res_g_mean
                df_t3.loc[df_t3[pressure_rounded_name] == p, r_error_name] = res_g_error

                df_t3.loc[df_t3[pressure_rounded_name] == p, r_bulk_name] = res_bulk
                df_t3.loc[df_t3[pressure_rounded_name] == p, r_bulk_mean] = res_bulk_mean
                df_t3.loc[df_t3[pressure_rounded_name] == p, r_bulk_error] = res_bulk_error

                # append cr-mean and cr-sem values of single pressure to x,y plotdata
                resistance_mean.append(res_cr_mean)
                resistance_error.append(res_cr_error)

                resistance_g_mean.append(res_g_mean)
                resistance_g_error.append(res_g_error)

                resistance_bulk_mean.append(res_bulk_mean)
                resistance_bulk_error.append(res_bulk_error)

                # df_t3.loc[df_t3[pressure_rounded_name] == p, cr_mean] = \
                #     res_cr_mean
                #
                # df_t3.loc[df_t3[pressure_rounded_name] == p, cr_mean] = \
                #     res_cr_mean

                df_list.append(df_t3)

            # forming x,y-value-lists into array
            # TODO: implement error-bars in graphs
            resistance_mean = np.asarray(resistance_mean)
            resistance_error = np.asarray(resistance_error)

            resistance_g_mean = np.asarray(resistance_g_mean)
            resistance_g_error = np.asarray(resistance_g_error)

            resistance_bulk_mean = np.asarray(resistance_bulk_mean)
            resistance_bulk_error = np.asarray(resistance_bulk_error)

            # graph --> res_mean over p (every cycle seperate)

            # plt.errorbar(pressures, resistance_mean, yerr=resistance_error, elinewidth=None, capsize=2, label=m + str(c))

            a[0][0].plot(pressures, resistance_g_mean, label = c)
            a[0][0].set_title('Resistance / Pressure')
            a[0][0].set_xlabel('Pressure [bar]')
            a[0][0].set_ylabel('Resistance [mOhm*cm²]')
            a[0][0].set_xlim([0, 30])
            a[0][0].set_ylim([0, 50])
            a[0][0].legend(bbox_to_anchor=(-0.55, 1, 0.4, 0), loc='upper left', mode='expand', ncol=3, fontsize='xx-small', title='Cycle')

            a[0][1].plot(pressures, resistance_bulk_mean)
            a[0][1].set_title('Bulk Resistance / Pressure')
            a[0][1].set_xlabel('Pressure [bar]')
            a[0][1].set_ylabel('Bulk Resistance [mOhm*cm²]')
            a[0][1].set_xlim([0, 30])
            a[0][1].set_ylim([0, 50])

            a[0][2].plot(pressures, resistance_mean)
            a[0][2].set_title('Contact Resistance / Pressure')
            a[0][2].set_xlabel('Pressure [bar]')
            a[0][2].set_ylabel('Contact Resistance [mOhm*cm²]')
            a[0][2].set_xlim([0, 30])
            a[0][2].set_ylim([-0.1, 0.1])

        for p in pressures:

            # declare empty y-value list for plotting --> gdl degradation
            ref_res_mean = []
            ref_res_g_mean = []
            ref_bulk_mean = []

            df_t2_p = df_t1[df_t1[pressure_rounded_name] == p]

            for c in cycles:

                df_t3_c = df_t2_p[df_t2_p['cycle'] == c]

                # calculate --> overall resistance
                cycle_res_g = (df_t3_c['U_ges-Th_U'] / df_t3_c['I_Ist / mA']) * 1000.0 * df_t2_p['Anpressfläche / cm²']

                # TODO: Hier muss res_g noch mittels korrekturfaktor anhand des GDL-Alters angepasst werden!

                # calculate --> contact resistance

                cycle_res = (cycle_res_g - df_t3_c['R_bulk / mOhm*cm²']) / 2.0

                cycle_res_bulk = df_t3_c['R_bulk / mOhm*cm²']

                # get mean resistance of cycle for specific pressure
                ref_res = cycle_res.mean()
                ref_res_g = cycle_res_g.mean()
                ref_res_bulk = cycle_res_bulk.mean()

                # append ref_res of cycle to y-value list
                ref_res_mean.append(ref_res)
                ref_res_g_mean.append(ref_res_g)
                ref_bulk_mean.append(ref_res_bulk)

            ref_res_mean = np.asarray(ref_res_mean)
            ref_res_g_mean = np.asarray(ref_res_g_mean)
            ref_bulk_mean = np.asarray(ref_bulk_mean)

            # graph --> res_mean over cylces (one specific pressure)

            a[1][0].plot(cycles, ref_res_g_mean, label=p)
            a[1][0].set_title('Resistance / Cycles')
            a[1][0].set_xlabel('Measurement Cycle')
            a[1][0].set_ylabel('Resistance [mOhm*cm²]')
            a[1][0].set_xlim([0, 60])
            a[1][0].set_ylim([0, 60])
            a[1][0].legend(bbox_to_anchor=(-0.55, 1, 0.2, 0), loc='upper left',
                           mode='expand', fontsize='small', title ='p [bar]')

            a[1][1].plot(cycles, ref_bulk_mean)
            a[1][1].set_title('Bulk-Resistance / Cycles')
            a[1][1].set_xlabel('Measurement Cycle')
            a[1][1].set_ylabel('Bulk-Resistance [mOhm*cm²]')
            a[1][1].set_xlim([0, 60])
            a[1][1].set_ylim([0, 60])

            a[1][2].plot(cycles, ref_res_mean)
            a[1][2].set_title('Contact Resistance / Cycles')
            a[1][2].set_xlabel('Measurement Cycle')
            a[1][2].set_ylabel('Contact Resistance [mOhm*cm²]')
            a[1][2].set_xlim([0, 60])
            a[1][2].set_ylim([-0.1, 0.1])



    df_result = pd.concat(df_list)
    df_import = df_result.sort_values(by=['Uhrzeit'])

    library_name = 'cr_library.csv'

    if os.path.isfile(library_name):
        with open(library_name, newline='') as file:
            if file.read().find(file_identifier) == -1:
                df_import.to_csv(library_name, mode='a', header=False, sep='\t')
            else:
                tk.messagebox.showinfo(title='Redundanz',
                                       message='Datei bereits im Archiv')
    else:
        df_import.to_csv(library_name, mode='w', header=True, sep='\t')

    # Formatiere Plot
    table_data = [
      ["Date", date],
      ["Sample", sample],
      ["GDL", gdl],
      ["Method", spec]
    ]

    table = a[0][0].table(cellText=table_data, colWidths=[.2, .5], loc='bottom',
                      bbox=[0.45, 0.75, 0.5, 0.2])



    for (row, col), cell in table.get_celld().items():
        if col == 0:
            cell.set_height(1.3)
            cell._loc = 'left'
            cell.set_text_props(ma='left', color='b', fontweight=50)
        elif col == 1:
            cell.set_height(1.3)
            cell._loc = 'right'
            cell.set_text_props(ma='right')

    plt.show()





