import pandas as pd
import numpy as np
from itertools import combinations
import time


def calc_elo_bycr(df):
  df['ELO_1'] = df.ch_nom_1.astype(str).map(elo).fillna(1000)
  df['ELO_2'] = df.ch_nom_2.astype(str).map(elo).fillna(1000)
  df['P_D'] = 1 / (1 + 10 ** ((df.ELO_2 - df.ELO_1)/400))
  df['D_ELO'] = 20 * (df.win - df['P_D']) 
  df['NEXT_ELO'] = df['ELO_1'] + df['D_ELO'] 
  
  #df.set_index('ch_nom1').to_dict()['NEXT_ELO']
  elo.update(df.groupby('ch_nom_1').NEXT_ELO.agg("mean").to_dict())
  #print(elo)
  return df.reset_index(drop=True)


# calculer une reference de course
# Chemin vers le fichier CSV (dans un répertoire nommé "data")
filename = 'pmu2014_c'

# Charger le fichier CSV dans un DataFrame
df = pd.read_csv(f'./data/{filename}.csv')

# Calculer qui gagne
df['win'] = (np.sign(df.ch_ordreArrivee_2 - df.ch_ordreArrivee_1) + 1.0) / 2.0

print(df)
elo = {}

bycr = df.groupby('aid_cr')

start_time = time.time()
r = bycr.apply(calc_elo_bycr)
elapsed_time = time.time() - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")

r.to_csv(f'./data/{filename}_e.csv', index=False)

'''
bycr = df_duplicated.groupby('aid_cr')
bycr.apply(lambda x : calc_elo_bycr(x))
'''
