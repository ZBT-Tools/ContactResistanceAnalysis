import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox


def store_library(file, sample, gdl1, gdl2, spec, ref):

    print(ref)

    # read datafile
    df_input = pd.read_csv(file, sep='\t', decimal=',', encoding='cp1252',
                           error_bad_lines=False)
    # round dataframa values
    df_input.round(2)

    # format dataframe
    # deleting unnecessary columns
    del df_input['R_ges / mOhm*cm²']
    del df_input['R_bulk / mOhm*cm²']
    del df_input['p_Kraftsensor / ?']
    del df_input['Weg Bürster']
    del df_input['Kraftsensor Poly']
    del df_input['Probendicke Poly']
    del df_input['Kraftsensor']
    del df_input['Probendicke']
    del df_input['U_ges 1']
    del df_input['U_Nadel 1']
    del df_input['U_ges 2']
    del df_input['U_Nadel 2']
    del df_input['Diff_U_ges/2']
    del df_input['Diff_U_Nadel/2']
    del df_input['Relais']

    df_input.drop(df_input.columns[[-1, ]], axis=1, inplace=True)


    # df_input.columns['date', 'time', 'commentary', 'pressure_sample[bar]',
    #                  'current[mA]', 'voltage[mV]', 'voltage_needle[mV]',
    #                  'voltage_th[mV]', 'voltage_needle_th[mV]',
    #                  'contact_area[cm2]', 'pressure[bar]']

    # rename columns of remaining dataframe
    df_input.rename(columns={df_input.iloc[0,0]:'date', 'Uhrzeit':'time',
                                'Kommentar':'commentary',
                                'p_Probe_Ist / bar':'pressure_sample[bar]',
                                'I_Ist / mA': 'current[mA]',
                                'U_ges / mV':'voltage[mV]',
                                'U_Nadel / mV':'voltage_needle[mV]',
                                'U_ges-Th_U': 'voltage_th[mV]',
                                'U_Nadel-Th_U':'voltage_needle_th[mV]',
                                'Anpressfläche / cm²':'contact_area[cm2]',
                                'p_Ist / bar':'pressure[bar]'},
                                inplace=True)

    # clear measurement artefacts (no current)
    df_input = df_input[df_input['current[mA]'] != 0]

    # fill empty/NaN celss with numerics (0)
    df_input.fillna(0, inplace=True)

    # define commentary / measurement
    commentary_name = 'commentary'
    measurement_name = 'measurement'

    # round pressures and append to df in seperate column
    pressure_rounded = df_input['pressure_sample[bar]'].round(decimals=0)

    # define additional columns for calculations result
    df_input.insert(len(df_input.columns), column='pressure_rounded[bar]',
                    value=pressure_rounded)

    cr_name = 'contact_resistance[mOhm*cm2]'
    df_input.insert(len(df_input.columns), cr_name, 0.0, True)

    cr_error_name = 'contact_resistance_error[mOhm*cm2]'
    df_input.insert(len(df_input.columns), cr_error_name, 0.0)

    cr_mean = 'contact_resistance_mean[mOhm*cm2]'
    df_input.insert(len(df_input.columns), cr_mean, 0.0)

    r_name = 'resistance[mOhm*cm2]'
    df_input.insert(len(df_input.columns), r_name, 0.0)

    r_mean = 'resistance_mean[mOhm*cm2]'
    df_input.insert(len(df_input.columns), r_mean, 0.0)

    r_error_name = 'resistance_error[mOhm*cm2]'
    df_input.insert(len(df_input.columns), r_error_name, 0.0)

    r_bulk_name = 'bulk_resistance[mOhm*cm2]'
    df_input.insert(len(df_input.columns), r_bulk_name, 0.0)

    r_bulk_mean = 'bulk_resistance_mean[mOhm*cm2]'
    df_input.insert(len(df_input.columns), r_bulk_mean, 0.0)

    r_bulk_error = 'bulk_resistance_error[mOhm*cm2]'
    df_input.insert(len(df_input.columns), r_bulk_error, 0.0)

    r_bulk_sub = 'bulk_resistance_sub[mOhm*cm2]'
    df_input.insert(len(df_input.columns), r_bulk_sub, 0.0)

    r_through = 'volume_resistance[mOhm*cm2]'
    df_input.insert(len(df_input.columns), r_through, 0.0)

    r_through_mean = 'volume_resistance_mean[mOhm*cm2]'
    df_input.insert(len(df_input.columns), r_through_mean, 0.0)

    r_through_error = 'volume_resistance_error[mOhm*cm2]'
    df_input.insert(len(df_input.columns), r_through_error, 0.0)

    corr = 'degradation_corr[mOhm*cm2]'
    df_input.insert(len(df_input.columns), corr, 0.0)

    cycle = 'cycle'
    df_input.insert(len(df_input.columns), cycle, 0.0)

    # seperate measurements by cycles

    z = 1
    rec = 0
    for i, v in df_input['pressure_rounded[bar]'].items():
        if v >= rec:

            df_input[cycle].loc[i] = z

            if df_input.loc[v, 'current[mA]'] < 600:
                rec = v
        else:
            z += 1
            rec = 0
            df_input[cycle].iloc[i] = z

    #get unique values as lists --> measurements / pressures / cycles
    measurements = np.unique(df_input[commentary_name].to_numpy())
    pressures = np.unique(pressure_rounded.to_numpy(dtype=int))
    cycles = np.unique(df_input['cycle'].to_numpy(dtype=int))

    #if ref is not 'Referenz' and gdl1 == 'H23':
    #     df_input.loc[(df_input['pressure_rounded[bar]'] <= 5) &
    #                  (df_input['cycle'] <= 60), corr] = 15.3
    #     df_input.loc[(df_input['pressure_rounded[bar]'] <= 10) &
    #                  (df_input['cycle'] <= 60), corr] = 11.4
    #     df_input.loc[(df_input['pressure_rounded[bar]'] <= 20) &
    #                  (df_input['cycle'] <= 60), corr] = 8.2
    #     df_input.loc[(df_input['pressure_rounded[bar]'] <= 30) &
    #                  (df_input['cycle'] <= 60), corr] = 6.8
    #
    # if ref is not 'Referenz' and gdl2 == '29BC':
    #     df_input.loc[(df_input['pressure_rounded[bar]'] <= 2.5) &
    #                  (df_input['cycle'] <= 60), corr] = 30
    #     df_input.loc[(df_input['pressure_rounded[bar]'] <= 5) &
    #                  (df_input['cycle'] <= 60), corr] = 20
    #     df_input.loc[(df_input['pressure_rounded[bar]'] <= 10) &
    #                  (df_input['cycle'] <= 60), corr] = 15
    #     df_input.loc[(df_input['pressure_rounded[bar]'] <= 20) &
    #                  (df_input['cycle'] <= 60), corr] = 10
    #     df_input.loc[(df_input['pressure_rounded[bar]'] <= 30) &
    #                  (df_input['cycle'] <= 60), corr] = 7.5
    #
    # else:
    #     df_input.loc[(df_input['pressure_rounded[bar]']) < 31 &
    #                  (df_input['cycle'] <= 100), corr] = 0

    #TODO: get correction to work!

    if ref is not 'Referenz' and gdl1 == 'H23':

        h23_ref = 'h23_reference.csv'
        df_h23 = pd.read_csv(h23_ref, sep='\t', decimal=',', encoding='cp1252',
                             error_bad_lines=False)

        #ref_pressure_rounded = df_h23['pressure_sample[bar]'].round(decimals=0)
        ref_pressures = np.unique(['pressure_rounded[bar'].to_numpy(dtype=int))

        #print(df_h23[r_mean])
        for c in cycles:
            df_input_1 = df_input[df_input['cycle'] == c]
            df_h23_1 = df_h23[df_h23['cycle'] == c]
            #print(df_h23_1[r_mean])
            for p in pressures:
                df_input_2 = df_input_1[df_input_1['pressure_rounded[bar]'] == p]
                df_h23_2 = df_h23_1[df_h23_1['pressure_rounded[bar]'] == p]
                print(df_h23_2[r_mean])
                correction_value = df_h23_2[r_mean]
                print(correction_value)
                df_input_2.loc[df_input_2['pressure_rounded[bar]'] == p, corr] = correction_value
                df_corr_list.append(df_input_2)

        df_input = pd.concat(df_corr_list)

    else:
        df_input.loc[(df_input['pressure_rounded[bar]']) < 31 &
                     (df_input['cycle'] <= 100), corr] = 0

    # create variable for storage in library --> file_identifier
    file_identifier = ref + ' ' + sample + ' ' + gdl1+gdl2 + spec

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
        df_t1.insert(2, measurement_name, measurement_identifier, True)

        # seperate measurement-df into different cycles
        for c in cycles:

            # df-slice of measurement-df with single 'cycle'
            df_t2_c = df_t1[df_t1[cycle] == c]

            # declare empty y / y-error-value list for plotting --> contact res
            resistance_mean = []
            resistance_error = []

            resistance_g_mean = []
            resistance_g_error = []

            resistance_bulk_mean = []
            resistance_bulk_error = []

            resistance_through_mean = []
            resistance_through_error = []

            # seperate 'cycle'-df into different pressures
            for p in pressures:

                # df-slice of 'cycle'-df with single pressure
                df_t3 = df_t2_c[df_t2_c['pressure_rounded[bar]'] == p]

                # calculate --> overall resistance
                res_g = (df_t3['voltage_th[mV]'] / df_t3['current[mA]']) * 1000.0 * df_t3['contact_area[cm2]']



                if spec == "m. Nadel":
                    res_bulk = (df_t3['voltage_needle[mV]'] / df_t3['current[mA]']) * 1000 * df_t3['contact_area[cm2]']
                else:
                    res_bulk = df_t3[r_bulk_sub] / 1

                res_through = ((df_t3['voltage_th[mV]'] / df_t3['current[mA]']) - (df_t3[corr]/1000)) * 1000 * df_t3['contact_area[cm2]']

                # calculate --> contact resistance

                res_cr = (((df_t3['voltage_th[mV]'] / df_t3['current[mA]']) -(df_t3[corr]/1000)-(df_t3['voltage_needle_th[mV]'] / df_t3['current[mA]'])) / 2.0) * 1000 * df_t3['contact_area[cm2]']

                #res_cr = (res_g - df_t3[corr] - res_bulk) / 2.0

                #res_cr = ((res_g - df_h23_cycle_pressure['Gesamtwiderstand / mOhm*cm2 - gemittelt']) - res_bulk) / 2.0

                # get mean- and sem-value of calculated resistance
                res_cr_mean = res_cr.mean()
                res_cr_error = res_cr.sem()

                res_g_mean = res_g.mean()
                res_g_error = res_g.sem()

                res_bulk_mean = res_bulk.mean()
                res_bulk_error = res_bulk.sem()

                res_through_mean = res_through.mean()
                res_through_error = res_through.sem()

                # write data --> cr-mean and cr-sem in df-slice
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, cr_name] = res_cr
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, cr_mean] = res_cr_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, cr_error_name] = res_cr_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, r_name] = res_g
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, r_mean] = res_g_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, r_error_name] = res_g_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, r_bulk_name] = res_bulk
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, r_bulk_mean] = res_bulk_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, r_bulk_error] = res_bulk_error

                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, r_through] = res_through
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, r_through_mean] = res_through_mean
                df_t3.loc[df_t3['pressure_rounded[bar]'] == p, r_through_error] = res_through_error

                # append cr-mean and cr-sem values of single pressure to x,y plotdata
                resistance_mean.append(res_cr_mean)
                resistance_error.append(res_cr_error)

                resistance_g_mean.append(res_g_mean)
                resistance_g_error.append(res_g_error)

                resistance_bulk_mean.append(res_bulk_mean)
                resistance_bulk_error.append(res_bulk_error)

                resistance_through_mean.append(res_through_mean)
                resistance_through_error.append(res_through_error)

                # df_t3.loc[df_t3['pressure_rounded[bar]'] == p, cr_mean] = \
                #     res_cr_mean
                #
                # df_t3.loc[df_t3['pressure_rounded[bar]'] == p, cr_mean] = \
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

            resistance_through_mean = np.asarray(resistance_through_mean)
            resistance_through_error = np.asarray(resistance_through_error)

            # graph --> res_mean over p (every 'cycle' seperate)

            # plt.errorbar(pressures, resistance_mean, yerr=resistance_error, elinewidth=None, capsize=2, label=m + str(c))

            a[0][0].plot(pressures, resistance_g_mean, label = c)
            a[0][0].set_title('Resistance / Pressure')
            a[0][0].set_xlabel('Pressure [bar]')
            a[0][0].set_ylabel('Resistance [mOhm*cm²]')
            a[0][0].set_xlim([0, max(pressures)])
            #a[0][0].set_ylim([0, max(resistance_g_mean)+1])
            a[0][0].legend(bbox_to_anchor=(-0.55, 1, 0.4, 0), loc='upper left', mode='expand', ncol=3, fontsize='xx-small', title='Cycle')

            a[0][1].plot(pressures, resistance_bulk_mean)
            a[0][1].set_title('Volume Resistance / Pressure')
            a[0][1].set_xlabel('Pressure [bar]')
            a[0][1].set_ylabel('Volume Resistance [mOhm*cm²]')
            a[0][1].set_xlim([0, max(pressures)])
            #a[0][1].set_ylim([0, max(resistance_through_mean)])

            a[0][2].plot(pressures, resistance_mean)
            a[0][2].set_title('Contact Resistance / Pressure')
            a[0][2].set_xlabel('Pressure [bar]')
            a[0][2].set_ylabel('Contact Resistance [mOhm*cm²]')
            a[0][2].set_xlim([0, max(pressures)])
            #a[0][2].set_ylim([min(resistance_mean)-0.1, max(resistance_mean)+0.1])

        for p in pressures:

            # declare empty y-value list for plotting --> gdl degradation
            ref_res_mean = []
            ref_res_g_mean = []
            ref_bulk_mean = []

            df_t2_p = df_t1[df_t1['pressure_rounded[bar]'] == p]

            for c in cycles:

                df_t3_c = df_t2_p[df_t2_p[cycle] == c]

                # calculate --> overall resistance
                cycle_res_g = (df_t3_c['voltage_th[mV]'] / df_t3_c['current[mA]']) * 1000.0 * df_t2_p['contact_area[cm2]']

                # TODO: Hier muss res_g noch mittels korrekturfaktor anhand des GDL-Alters angepasst werden!

                # calculate --> contact resistance


                cycle_res_bulk = (df_t3_c['voltage_needle_th[mV]'] / df_t3_c['current[mA]']) * 1000 * df_t3_c['contact_area[cm2]']

                # cycle_res = (((df_t3_c['U_ges-Th_U'] / df_t3_c['I_Ist / mA']) -
                #               (df_t3_c['U_Nadel-Th_U'] / df_t3_c['I_Ist / mA'])) / 2.0) * 1000 * df_t3_c['Anpressfläche / cm²']
                cycle_res = (cycle_res_g - cycle_res_bulk) / 2.0



                # get mean resistance of 'cycle' for specific pressure
                ref_res = cycle_res.mean()
                ref_res_g = cycle_res_g.mean()
                ref_res_bulk = cycle_res_bulk.mean()

                # append ref_res of 'cycle' to y-value list
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
            a[1][0].set_xlim([0, max(cycles)])
            #a[1][0].set_ylim([0, max(ref_res_g_mean)+10])
            a[1][0].legend(bbox_to_anchor=(-0.55, 1, 0.2, 0), loc='upper left',
                           mode='expand', fontsize='small', title ='p [bar]')

            a[1][1].plot(cycles, ref_bulk_mean)
            a[1][1].set_title('Bulk-Resistance / Cycles')
            a[1][1].set_xlabel('Measurement Cycle')
            a[1][1].set_ylabel('Bulk-Resistance [mOhm*cm²]')
            a[1][1].set_xlim([0, max(cycles)])
            #a[1][1].set_ylim([0, max(ref_bulk_mean)+10])

            a[1][2].plot(cycles, ref_res_mean)
            a[1][2].set_title('Contact Resistance / Cycles')
            a[1][2].set_xlabel('Measurement Cycle')
            a[1][2].set_ylabel('Contact Resistance [mOhm*cm²]')
            a[1][2].set_xlim([0, max(cycles)])
            #a[1][2].set_ylim([min(ref_res_mean)-0.1, max(ref_res_mean)+0.1])



    df_result = pd.concat(df_list)
    df_import = df_result.sort_values(by=['time'])
    df_import2 = df_import.round(2)

    library_name = 'cr_library.csv'

    if os.path.isfile(library_name):
        with open(library_name, newline='') as file:
            if file.read().find(file_identifier) == -1:
                df_import2.to_csv(library_name, mode='a', header=False, sep='\t')
            else:
                tk.messagebox.showinfo(title='Redundanz',
                                       message='Datei bereits im Archiv')
    else:
        df_import2.to_csv(library_name, mode='w', header=True, sep='\t')

    # Formatiere Plot
    table_data = [
      ["Sample", sample],
      ["GDL", gdl1+gdl2],
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





