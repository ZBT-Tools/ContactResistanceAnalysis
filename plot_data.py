import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_data(meas):

    print(meas)
    df_data = pd.read_csv('cr_library.csv', sep='\t')
    # df_data.rename(index={2: 'Messung'})
    df_data = df_data[df_data['Messung'] == meas]
    print(df_data)

    df_temp = df_data['p_Probe_Ist / bar'].round(decimals=0)
    pressure_rounded = 'p_Probe_Ist_rounded / bar'
    #df_data.insert(len(df_data.columns), column=pressure_rounded, value=df_temp)

    #measurements = np.unique(df_compl['Kommentar'].to_numpy())
    pressures = np.unique(df_temp.to_numpy(dtype=int))

    # for m in measurements:
    #     df_t1 = df_compl[df_compl['Kommentar'] == m]
    #     samplespec = date + ' ' + sample + ' ' + gdl + ' ' + spec + ' ' + m
    #     df_t1.insert(1, 'Messung', samplespec, True)
    #
    #     if os.stat("cr_library.csv").st_size != 0:
    #         if open('cr_library.csv', 'r').read().find(samplespec) == -1:
    #             df_t1.to_csv('cr_library.csv', mode='a', header=False)
    #         else:
    #             tk.messagebox.showinfo(title='Redundanz', message='Messung bereits im Archiv')
    #     else:
    #         df_t1.to_csv('cr_library.csv', mode='w', header=True)

    resistance_mean = []
    resistance_error = []

    for p in pressures:
        df_t2 = df_data[df_data[pressure_rounded] == p]
        res_g = (df_t2['U_ges-Th_U'] / df_t2['I_Ist / mA']) * 1000 * df_t2['Anpressfläche / cm²']

        #TODO: hier muss res_g noch mittels korrekturfaktor an Hand des GDL alters angepasst werden!

        res_cr = (res_g - df_t2['R_bulk / mOhm*cm²']) / 2
        resistance_mean.append(res_cr.mean())
        resistance_error.append(res_cr.sem())

    resistance_mean = np.asarray(resistance_mean)
    resistance_error = np.asarray(resistance_error)

    #
    # plt.errorbar(pressures, resistance_mean, yerr=resistance_error, elinewidth=None, capsize=2, label=meas)
    #
    # plt.xlabel('Contact Pressure / bar')
    # plt.ylabel('Contact Resistance / mOhm*cm²')
    # plt.title('Contact Resistance')
    # plt.legend()
    # plt.show()

    return pressures, resistance_mean



