
import pandas as pd
import time
import numpy as np

import combine
import elo1
import skills



def prepare(df):
    
    '''start_time = time.time()
    df = combine.clean(df)
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    
    start_time = time.time()
    df = combine.un_vs_un(df)
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")'''
   
    start_time = time.time()
    df = skills.calc_oskill(df)
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    return df

def pct_place(df):
    n = len(df)
    np = len(df[df.ch_estplace_1])
    ng = len(df[df.ch_estgagant_1])
    print(f'placé {100 * np / n}%  [{np}/{n}] - gagnant {100 * ng / n}% [{ng}/{n}]')

'''df = pd.read_csv('./data/2015cc.csv')
#df = pd.read_csv('./data/volcania_p.csv')
df = prepare(df)
#df.to_csv('./data/volcania_os.csv', index=False)
df.to_csv('./data/2015_os.csv', index=False)'''



##df[df.ch_nom_1 == 'VALEUR DANOVER'].to_csv('test.csv')

df = pd.read_csv('./data/2015_os.csv')
result = df[df.ch_dernierRapportDirect_rapport_1 > 0].groupby(['aid_cr', 'ch_nom_1']).first().reset_index()
print(len(result))
result['OS_R'] = result.groupby('aid_cr')['OS_ORD_1'].rank(ascending=False)
result['COTE_R'] = result.groupby('aid_cr')['ch_dernierRapportDirect_rapport_1'].rank()
result['CHGAINC_R'] = result.groupby('aid_cr')['ch_gainsParticipant_gainsCarriere_1'].rank(ascending=False)
result['CHGAING_R'] = result.groupby('aid_cr')['ch_gainsParticipant_gainsVictoires_1'].rank(ascending=False)
#result.to_csv('./data/ranked.csv', index=False)

pct_place(result[result.OS_R == 1.0])
pct_place(result[result.OS_R == 2.0])
pct_place(result[result.OS_R == 3.0])
pct_place(result[result.OS_R == 10.0])
print('--COTE_R')
pct_place(result[result.COTE_R == 1.0])
pct_place(result[result.COTE_R == 2.0])
pct_place(result[result.COTE_R == 3.0])
pct_place(result[result.COTE_R == 10.0])
print('--CHGAINC_R')
pct_place(result[result.CHGAINC_R == 1.0])
pct_place(result[result.CHGAINC_R == 2.0])
pct_place(result[result.CHGAINC_R == 3.0])
pct_place(result[result.CHGAINC_R == 10.0])
print('--CHGAING_R')
pct_place(result[result.CHGAING_R == 1.0])
pct_place(result[result.CHGAING_R == 2.0])
pct_place(result[result.CHGAING_R == 3.0])
pct_place(result[result.CHGAING_R == 10.0])
print('--')
pct_place(result[(result.COTE_R == 1.0) & (result.OS_R == 1.0)])
pct_place(result[(result.COTE_R == 2.0) & (result.OS_R == 1.0)])
pct_place(result[(result.COTE_R == 3.0) & (result.OS_R == 1.0)])
pct_place(result[(result.COTE_R == 10.0) & (result.OS_R == 1.0)])


