
import pandas as pd
import time

import combine
import elo1



def prepare(df):
    start_time = time.time()
    #df = combine.clean(df)
    #df = combine.un_vs_un(df)
    #df = elo1.calc_elo(df, 'ch_nom')
    df = elo1.calc_elo(df, 'ch_driver')
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    return df

def pct_place(df):
    n = len(df)
    np = len(df[df.ch_estplace_1])
    ng = len(df[df.ch_estgagant_1])
    print(f'placé {100 * np / n}%  [{np}/{n}] - gagnant {100 * ng / n}% [{ng}/{n}]')


df = pd.read_csv('./data/2015cce2.csv')
#df = prepare(df)
#df.to_csv('./data/2015cce2.csv')

##df[df.ch_nom_1 == 'VALEUR DANOVER'].to_csv('test.csv')


'''result = result = df[df.ch_dernierRapportDirect_rapport_1 > 0].groupby(['aid_cr', 'ch_nom_1']).first().reset_index()
print(len(result))
result['ELOC_R'] = result.groupby('aid_cr')['ELO_ch_nom_1'].rank(ascending=False)
result['ELOD_R'] = result.groupby('aid_cr')['ELO_ch_driver_1'].rank(ascending=False)
result['COTE_R'] = result.groupby('aid_cr')['ch_dernierRapportDirect_rapport_1'].rank()

pct_place(result[result.ELOD_R == 1.0])
pct_place(result[result.ELOD_R == 2.0])
pct_place(result[result.ELOD_R == 3.0])
pct_place(result[result.ELOD_R == 10.0])
print('--')
pct_place(result[(result.ELOD_R == 1.0) & (result.ELOC_R == 1.0)])
pct_place(result[(result.ELOD_R == 2.0) & (result.ELOC_R == 2.0)])
pct_place(result[(result.ELOD_R == 3.0) & (result.ELOC_R == 3.0)])
pct_place(result[(result.ELOD_R == 10.0) & (result.ELOC_R == 10.0)])
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
pct_place(result[(result.COTE_R == 1.0) & (result.ELOD_R == 1.0)])
pct_place(result[(result.COTE_R == 2.0) & (result.ELOD_R == 1.0)])
pct_place(result[(result.COTE_R == 3.0) & (result.ELOD_R == 1.0)])
pct_place(result[(result.COTE_R == 10.0) & (result.ELOD_R == 1.0)])'''

