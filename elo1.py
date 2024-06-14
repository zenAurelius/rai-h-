import pandas as pd
import numpy as np
from itertools import combinations


def calc_elo_bycr(df):
  print(df)
  df['ELO_1'] = df.CH_NOM_1.map(elo).fillna(1000)
  df['ELO_2'] = df.CH_NOM_2.map(elo).fillna(1000)
  df['P_D'] = 1 / (1 + 10 ** ((df.ELO_1 - df.ELO_2)/400))
  df['D_ELO'] = 20 * (((df.WIN + 1) / 2) - df['P_D']) 
  for index, row in df.iterrows():
    print(row["CH_NOM_1"], " - ", row["CH_NOM_2"])
  print(df[['CH_NOM_1', 'ELO_1', 'ELO_2', 'P_D', 'WIN', 'D_ELO']])
    


# la fonction qui combine les participations deux à deux, appelé sur un groupby,
# le df param est l'ensemble des participations d'une course
def combine(df) :
  # ici on recupère une liste des différentes combinaison d'index
  cc = list(combinations(df.index, 2))
  dfs = []
  # pour chaque combinaison c, on recupère les deux lignes dans un df, on ajoute 
  # une clé spécifique à cette combinaison et on ajoute ce df dans la liste des df
  for i, c in enumerate(cc) :
    dfc = df.loc[c,:]
    dfc['CF_REF'] = dfc.aid_cr + f'_{i:02.0f}'
    dfs.append(dfc) 
  
  # la sortie correspond à la concaténation de toutes les combinaisons
  out = pd.concat(dfs)
  return out



def un_vs_un():
  # Grouper les enregistrements par valeur dans la colonne CR_REF
  grouped = df.groupby('aid_cr')

  crout = grouped.apply(lambda x : combine(x))
  crout = crout.drop(columns=['aid_cr']).reset_index()

  print('crout')
  print(crout)

  # AGGREGATION DES COMBINAISONS
  # pour l'instant on a deux lignes par combinaison, il faut les aggréger selon 
  # deux opérations, soit en liste (quand il y a deux valeurs différentes attendues)
  # soit en first (quand c'est la même valeur pour les deux lignes)
  part_col = [c for c in all_col if not c.startswith('cr')]
  opes = [ (x, list) if x in part_col else (x, 'first') for x in all_col]
  # on regroupe par combinaison et on aggrege
  gp_cf = crout.groupby('CF_REF')
  agg1 = gp_cf.agg(dict(opes))
  # pour chaque ligne "list", on explose en deux colonnes (x_1 et x_2)
  for c in part_col:
    dest_col = [c + '_' + str(i) for i in range(1, 3)]
    print(dest_col)
    agg1[dest_col] = pd.DataFrame(agg1[c].tolist(), index= agg1.index)

  agg1 = agg1.reset_index()
  print('-- agg--')
  print(agg1)

  # Obtenez la liste des colonnes se terminant par '_1'


  # Créez une nouvelle DataFrame en dupliquant chaque ligne et en transférant les valeurs entre les colonnes _1 et _2
  df_duplicated = pd.concat([agg1,
                            agg1.rename(columns=lambda c : c.replace('_1', '_2') if c.endswith('_1') else c.replace('_2', '_1') if c.endswith('_2') else c )],
                            ignore_index=True)
  df_duplicated.sort_values(by=['CF_REF'], inplace=True)
  df_duplicated['WIN'] = (df_duplicated['ch_ordreArrivee_2'] > df_duplicated['ch_ordreArrivee_1']).astype(int) - (df_duplicated['ch_ordreArrivee_1'] > df_duplicated['ch_ordreArrivee_2']).astype(int)


  # Affichez la DataFrame dupliquée
  print('df_duplicated')
  print(df_duplicated)
  df_duplicated.to_csv('1vs1.csv')


def clean(df):
  # Afficher les premières lignes du DataFrame avant la modification
  print("Avant la modification :")
  print(df.head())
  df['cr_date'] =  pd.to_datetime(df['cr_heureDepart'], unit='ms').dt.strftime("%y%m%d")
  df['ch_ordreArrivee'] = df['ch_ordreArrivee'].replace(np.nan, 11.0)
  df['aid_cr'] = df.cr_date + 'R' + df.cr_numReunion.astype(str).str.zfill(2) + 'C' + df.cr_numOrdre.astype(str).str.zfill(2)

  # les différentes colonnes qu'on veut garder, reparties dans des colonnes liées à la course, à la participation ou au calcul du target
  cr_col = ['aid_cr', 'cr_libelleCourt']
  ch_col = ['ch_nom', 'ch_numPmu']
  tg_col = ['ch_ordreArrivee']
  all_col = cr_col + ch_col + tg_col
  return df[all_col]


# calculer une reference de course
# Chemin vers le fichier CSV (dans un répertoire nommé "data")
filename = 'pmu2014'

# Charger le fichier CSV dans un DataFrame
df = pd.read_csv(f'./data/{filename}.csv')

df = clean(df)
df.to_csv(f'./data/{filename}c.csv', index=False)

'''
elo = {}
bycr = df_duplicated.groupby('aid_cr')
bycr.apply(lambda x : calc_elo_bycr(x))
'''
