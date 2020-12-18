import pandas as pd

file= 'C:/Users/Kapp/Desktop/KW - Messungen/FEM/20201217/fem_1_Ni'

df_input = pd.read_csv(file, sep='\t', decimal=',', encoding='cp1252',
                           error_bad_lines=False)

print(df_input)