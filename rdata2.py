import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#einlesen der Daten in Dataframe --> df_compl
df_compl = pd.read_csv('test', sep='\t', decimal=',', encoding='cp1252', error_bad_lines=False)

#separieren der ersten Messreihe in eigens Dataframe --> df_m1
df_compl = df_compl[df_compl['I_Ist / mA'] != 0]


#print(measurements)

#df_m1 = df_m1[df_m1['Kommentar'] == 'Messung I']


#Ermitteln der Druckmessreihe
#Drücke auf ganze Zahlen runden und in seperates Dataframe einfügen

df2 = df_compl['p_Probe_Ist / bar'].round(decimals=0)

#Umebennenung der Druckspalte mit gerundeten Werten

pressure_rounded = 'p_Probe_Ist_rounded / bar'
measurement_split = 'Kommentar'

#Spalte mit gerundetem Druck wird an die letzte Spalte des Dataframes der Messung I angefügt

df_compl.insert(len(df_compl.columns), column=pressure_rounded, value=df2)

#Ermitteln der einzigartigen Drücke --> Druckmessreihe

measurements = np.unique(df_compl['Kommentar'].to_numpy())
pressures = np.unique(df2.to_numpy(dtype=int))




#Für jeden Druck (5 Zyklen / 4 Ströme) werden die jeweiligen Widerstände gemittelt und an die Listen übergeben
for m in measurements:
  df_t1 = df_compl[df_compl['Kommentar'] == m]
  # Deklarieren der benötigten Listen für die Darstellung im Diagramm (y-Achse)
  resistance_mean = []
  resistance_error = []
  for p in pressures:
    df_t2 = df_t1[df_t1[pressure_rounded] == p]
    res_g = (df_t2['U_ges-Th_U'] / df_t2['I_Ist / mA']) * 1000 * df_t2['Anpressfläche / cm²']

    #hier muss res_g noch mittels korrekturfaktor an Hand des GDL alters angepasst werden!

    res_cr = (res_g - df_t2['R_bulk / mOhm*cm²']) / 2
    resistance_mean.append(res_cr.mean())
    resistance_error.append(res_cr.sem())
  resistance_mean = np.asarray(resistance_mean)
  resistance_error = np.asarray(resistance_error)
  plt.errorbar(pressures, resistance_mean, yerr=resistance_error, elinewidth=None, capsize=2, label=m)

description = 'Datum:\t\nE1GDL:\nProbe:\nMessmethode:'
plt.text(25, 100, description, horizontalalignment='right', verticalalignment='center')

plt.xlabel('Contact Pressure / bar')
plt.ylabel('Contact Resistance / mOhm*cm²')
plt.title('Contact Resistance')
plt.legend()
plt.show()





import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np

#einlesen der Daten in Dataframe --> df_compl
df_compl = pd.read_csv('test', sep='\t', decimal=',', encoding='cp1252', error_bad_lines=False)

#separieren der ersten Messreihe in eigens Dataframe --> df_m1
df_m1 = df_compl[df_compl['I_Ist / mA'] != 0]
df_m1 = df_m1[df_m1['Kommentar'] == 'Messung I']


#Ermitteln der Druckmessreihe
#Drücke auf ganze Zahlen runden und in seperates Dataframe einfügen

df3 = df_m1['p_Probe_Ist / bar'].round(decimals=0)

#Umebennenung der Druckspalte mit gerundeten Werten

pressure_rounded = 'p_Probe_Ist_rounded / bar'

#Spalte mit gerundetem Druck wird an die letzte Spalte des Dataframes der Messung I angefügt

df_m1.insert(len(df_m1.columns), column=pressure_rounded, value=df3)

#Ermitteln der einzigartigen Drücke --> Druckmessreihe

pressures = np.unique(df3.to_numpy(dtype=int))

#Deklarieren der benötigten Listen für die Darstellung im Diagramm (y-Achse)
resistance_mean = []
resistance_error = []

#Für jeden Druck (5 Zyklen / 4 Ströme) werden die jeweiligen Widerstände gemittelt und an die Listen übergeben

for p in pressures:
    df_i = df_m1[df_m1[pressure_rounded] == p]
    res_g = (df_i['U_ges / mV'] / df_i['I_Ist / mA'])*1000*df_i['Anpressfläche / cm²']

    #hier muss res_g noch mittels korrekturfaktor an Handdes GDL alters angepasst werden!

    res_cr = (res_g - df_i['R_bulk / mOhm*cm²']) / 2
    resistance_mean.append(res_cr.mean())
    resistance_error.append(res_cr.sem())

resistance_mean = np.asarray(resistance_mean)
resistance_error = np.asarray(resistance_error)

plt.errorbar(pressures, resistance_mean, yerr=resistance_error, label='Contact Resistance')
plt.xlabel('Contact Pressure / bar')
plt.ylabel('Contact Resistance / mOhm')
plt.title('Contact Resistance')
plt.legend()
plt.show()
