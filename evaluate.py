
import pandas as pd
import time
import numpy as np

import combine
import elo1
import skills





def pct_place(df):
    n = len(df)
    npl = len(df[df.ch_estplace_1])
    nga = len(df[df.ch_estgagnant_1])
    print(f'placé {100 * npl / n}%  [{npl}/{n}] - gagnant {100 * nga / n}% [{nga}/{n}]')
    df['gain_gagnant'] = np.where(df['ch_estgagnant_1'], df['ch_dernierRapportDirect_rapport_1']-1, -1)
    print(f'gain gagnant = {df.gain_gagnant.sum()}')


def evaluate_indicateur(df, idname, sens):
    ntot = len(df)
    # 1. evaluation brute en 1c1
    print('* evaluation brute 1c1')
    ntrue = len(df[(df['ch_ordreArrivee_1'] < df['ch_ordreArrivee_2'])])
    nfalse = len(df[(df['ch_ordreArrivee_1'] > df['ch_ordreArrivee_2'])])
    print(f'[dummy] true = {100 * ntrue / ntot} - false = {100 * nfalse / ntot}')  
    ntrue = 2*len(df[(df['ch_ordreArrivee_1'] < df['ch_ordreArrivee_2']) & (df['ch_dernierRapportDirect_rapport_1'] < df['ch_dernierRapportDirect_rapport_2'])])
    nfalse = 2*len(df[(df['ch_ordreArrivee_1'] < df['ch_ordreArrivee_2']) & (df['ch_dernierRapportDirect_rapport_1'] > df['ch_dernierRapportDirect_rapport_2'])])
    print(f'[cote] true = {100 * ntrue / ntot} - false = {100 * nfalse / ntot}')
    ntrue = 2*len(df[(df['ch_ordreArrivee_1'] < df['ch_ordreArrivee_2']) & (df[f'{idname}_1'] > df[f'{idname}_2'])])
    nfalse = 2*len(df[(df['ch_ordreArrivee_1'] > df['ch_ordreArrivee_2']) & (df[f'{idname}_1'] > df[f'{idname}_2'])])
    print(f'[{idname}] true = {100 * ntrue / ntot} - false = {100 * nfalse / ntot}')
    
    # 2. evalutation par ordre
    # filtre sur les cas avec cotes - reset
    #result = df[df.ch_dernierRapportDirect_rapport_1 > 0].groupby(['aid_cr', 'ch_nom_1']).first().reset_index()


##df[df.ch_nom_1 == 'VALEUR DANOVER'].to_csv('test.csv')

df = pd.read_csv('./data/pmu2016cc_os.csv')
evaluate_indicateur(df, 'OS_ORD', '')
# result = df[df.ch_dernierRapportDirect_rapport_1 > 0].groupby(['aid_cr', 'ch_nom_1']).first().reset_index()
# print(len(result))
# bycr = result.groupby('aid_cr')

# result['OS_ORD_MEAN'] = bycr['OS_ORD_1'].transform('mean')
# result['OS_ORD_DT'] = result['OS_ORD_1'] / result['OS_ORD_MEAN']
# result['OS_R'] = bycr['OS_ORD_DT'].rank(ascending=False)
# result['COTE_R'] = bycr['ch_dernierRapportDirect_rapport_1'].rank()
# result['CHGAINC_R'] = bycr['ch_gainsParticipant_gainsCarriere_1'].rank(ascending=False)
# result['CHGAING_R'] = bycr['ch_gainsParticipant_gainsVictoires_1'].rank(ascending=False)
# #result.to_csv('./data/ranked.csv', index=False)

# pct_place(result[result.OS_R == 1.0].copy())
# pct_place(result[result.OS_R == 2.0].copy())
# pct_place(result[result.OS_R == 3.0].copy())
# pct_place(result[result.OS_R == 10.0].copy())
# print('--COTE_R')
# pct_place(result[result.COTE_R == 1.0].copy())
# pct_place(result[result.COTE_R == 2.0].copy())
# pct_place(result[result.COTE_R == 3.0].copy())
# pct_place(result[result.COTE_R == 10.0].copy())
# print('--CHGAINC_R')
# pct_place(result[result.CHGAINC_R == 1.0].copy())
# pct_place(result[result.CHGAINC_R == 2.0].copy())
# pct_place(result[result.CHGAINC_R == 3.0].copy())
# pct_place(result[result.CHGAINC_R == 10.0].copy())
# print('--CHGAING_R')
# pct_place(result[result.CHGAING_R == 1.0].copy())
# pct_place(result[result.CHGAING_R == 2.0].copy())
# pct_place(result[result.CHGAING_R == 3.0].copy())
# pct_place(result[result.CHGAING_R == 10.0].copy())
# print('--')
# pct_place(result[(result.COTE_R == 1.0) & (result.OS_R == 1.0)].copy())
# pct_place(result[(result.COTE_R == 2.0) & (result.OS_R == 1.0)].copy())
# pct_place(result[(result.COTE_R == 3.0) & (result.OS_R == 1.0)].copy())
# pct_place(result[(result.COTE_R == 4.0) & (result.OS_R == 1.0)].copy())
# pct_place(result[(result.COTE_R == 5.0) & (result.OS_R == 1.0)].copy())
# pct_place(result[(result.COTE_R == 10.0) & (result.OS_R == 1.0)].copy())

