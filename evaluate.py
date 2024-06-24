
import pandas as pd
import time
import numpy as np

import combine
import elo1
import skills



def prepare(df):
    start_time = time.time()
    df = combine.clean(df)
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    
    start_time = time.time()
    df = combine.un_vs_un(df)
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    #df = elo1.calc_elo(df, 'ch_nom')
    #df = elo1.calc_elo(df, 'ch_driver')
    
    start_time = time.time()
    df = skills.calc_oskill(df)
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    return df

def pct_place(df):
    n = len(df)
    np = len(df[df.ch_estplace_1])
    ng = len(df[df.ch_estgagnant_1])
    print(f'placé {100 * np / n}%  [{np}/{n}] - gagnant {100 * ng / n}% [{ng}/{n}]')


'''df = pd.read_csv('./data/pmu2016.csv')
df = prepare(df)
df.to_csv('./data/pmu2016cc_os.csv', index=False)'''



##df[df.ch_nom_1 == 'VALEUR DANOVER'].to_csv('test.csv')

df = pd.read_csv('./data/pmu2016cc_os.csv')
result = result = df[df.ch_dernierRapportDirect_rapport_1 > 0].groupby(['aid_cr', 'ch_nom_1']).first().reset_index()
result['ch_estplace_1'] = (result['ch_ordreArrivee_1'] < 3) | ((result['ch_ordreArrivee_1'] == 3) & (result['cr_nombreDeclaresPartants'] > 7))
print(len(result))
result['ELOC_R'] = result.groupby('aid_cr')['OS_MU_CH1'].rank(ascending=False)
result['ELOD_R'] = result.groupby('aid_cr')['OS_MU_DV1'].rank(ascending=False)
result['COTE_R'] = result.groupby('aid_cr')['ch_dernierRapportDirect_rapport_1'].rank()
#result.to_csv('./data/ranked.csv', index=False)

pct_place(result[result.ELOC_R == 1.0])
pct_place(result[result.ELOC_R == 2.0])
pct_place(result[result.ELOC_R == 3.0])
pct_place(result[result.ELOC_R == 10.0])
print('--')
'''pct_place(result[(result.ELOD_R == 1.0) & (result.ELOC_R == 1.0)])
pct_place(result[(result.ELOD_R == 2.0) & (result.ELOC_R == 2.0)])
pct_place(result[(result.ELOD_R == 3.0) & (result.ELOC_R == 3.0)])
pct_place(result[(result.ELOD_R == 10.0) & (result.ELOC_R == 10.0)])'''
print('--')
pct_place(result[result.COTE_R == 1.0])
pct_place(result[result.COTE_R == 2.0])
pct_place(result[result.COTE_R == 3.0])
pct_place(result[result.COTE_R == 10.0])
print('--')
pct_place(result[(result.COTE_R == 1.0) & (result.ELOC_R == 1.0)])
pct_place(result[(result.COTE_R == 2.0) & (result.ELOC_R == 1.0)])
pct_place(result[(result.COTE_R == 3.0) & (result.ELOC_R == 1.0)])
pct_place(result[(result.COTE_R == 10.0) & (result.ELOC_R == 1.0)])
print('--')
'''
pct_place(result[(result.COTE_R == 1.0) & (result.ELOD_R == 1.0)])
pct_place(result[(result.COTE_R == 2.0) & (result.ELOD_R == 1.0)])
pct_place(result[(result.COTE_R == 3.0) & (result.ELOD_R == 1.0)])
pct_place(result[(result.COTE_R == 10.0) & (result.ELOD_R == 1.0)])'''

