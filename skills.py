import pandas as pd
import numpy as np

'''df = pd.read_csv('./data/volcania_p.csv')
df =df[['aid_cr', 'ch_nom_1', 'ch_driver_1', 'ch_ordreArrivee_1', 'ch_nom_2', 'ch_driver_2', 'ch_ordreArrivee_2']]
df.to_csv('./data/volcania_s.csv', index=False)'''



'''params= {'dsg':float(25/3), 'dmu':float(25), 'tau':float(25.0 / 300.0), 'beta':float(25.0 / 6.0)}
b_sg = {}
b_mu = {}'''


def calc_oskill_bycr(df, os_sg, os_mu):
    
    dsg = float(25/3)
    dmu = float(25)
    tsq = float(25.0 / 300.0) ** 2
    for i in range(1, 3):
        # init sigma / mu -ok
        df[f'OS_SG_CH{i}'] = df[f'ch_nom_{i}'].astype(str).map(os_sg).fillna(dsg)
        df[f'OS_SG_DV{i}'] = df[f'ch_driver_{i}'].astype(str).map(os_sg).fillna(dsg) 
        df[f'OS_MU_CH{i}'] = df[f'ch_nom_{i}'].astype(str).map(os_mu).fillna(dmu)
        df[f'OS_MU_DV{i}'] = df[f'ch_driver_{i}'].astype(str).map(os_mu).fillna(dmu) 

        # Correct Sigma With Tau -ok
        df[f'S_SGC_CH{i}'] = np.sqrt(df[f'OS_SG_CH{i}'] ** 2 + tsq)
        df[f'S_SGC_DV{i}'] = np.sqrt(df[f'OS_SG_DV{i}'] ** 2 + tsq)

        # Sigma et Mu de chaque equipe = somme des Sigma/Mu de chaque players -ok
        df[f'S_SGSQ_{i}'] = df[f'S_SGC_CH{i}'] ** 2 + df[f'S_SGC_DV{i}'] ** 2 
        df[f'S_MU_{i}'] = df[f'OS_MU_CH{i}'] + df[f'OS_MU_DV{i}']
  
    # Calcul "C" = sqrt(somme pour toutes les equipes de Sigma^2 + beta^2) -ok
    bsq = float(25.0 / 6.0) ** 2
    c = np.sqrt(df['S_SGSQ_1'] + df['S_SGSQ_2'] + 2 * bsq)

    for i in range(1, 3):
        # Calcul "sumQ" -ok
        df[f'S_SUMQT_{i}'] = np.exp(df[f'S_MU_{i}']/c)

        #Calcul "A" -ok
        df[f'S_A_{i}'] = 1
        df.loc[df['win'] == 0.5, f'S_A_{i}'] = 2

    df[f'S_SUMQ_1'] = df[f'S_SUMQT_1'] + np.where(df['win'] >= 0.5, df[f'S_SUMQT_1'], 0)
    df[f'S_SUMQ_2'] = df[f'S_SUMQT_2'] + np.where(df['win'] <= 0.5, df[f'S_SUMQT_2'], 0)

    #i = 1; q = 1
    df['S_DELTA_11'] =  df['S_SUMQT_1'] / df['S_SUMQ_1'] * (1 - df['S_SUMQT_1'] / df['S_SUMQ_1']) / df['S_A_1']
    df['S_DELTA_12'] =  df['S_SUMQT_1'] / df['S_SUMQ_2'] * (1 - df['S_SUMQT_1'] / df['S_SUMQ_2']) / df['S_A_2']
    df['S_DELTA_12'] = np.where(df['win'] <= 0.5, df['S_DELTA_12'], 0)
    df['S_DELTA_1'] = (np.sqrt(df['S_SGSQ_1']) / c) * (df['S_DELTA_11'] + df['S_DELTA_12']) * df['S_SGSQ_1'] / c ** 2

    df['S_OMG_11'] = (1 - df['S_SUMQT_1'] / df['S_SUMQ_1']) / df['S_A_1']
    df['S_OMG_12'] = (df['S_SUMQT_1'] / df['S_SUMQ_2']) / df['S_A_2']
    df['S_OMG_12'] = np.where(df['win'] <= 0.5, df['S_OMG_12'], 0)
    df['S_OMG_1'] = (df['S_OMG_11'] - df['S_OMG_12']) * df['S_SGSQ_1'] / c


    df['S_N_MU_CH1'] = df['OS_MU_CH1'] + (df['S_OMG_1'] * df['S_SGC_CH1'] ** 2 / df['S_SGSQ_1'])
    df['S_N_MU_DV1'] = df['OS_MU_DV1'] + (df['S_OMG_1'] * df['S_SGC_DV1'] ** 2 / df['S_SGSQ_1'])
    df['S_N_SG_CH1'] = df['S_SGC_CH1'] * np.sqrt(np.maximum(1 - (df['S_DELTA_1'] * df['S_SGC_CH1']**2 / df['S_SGSQ_1']), 0.01))
    df['S_N_SG_DV1'] = df['S_SGC_DV1'] * np.sqrt(np.maximum(1 - (df['S_DELTA_1'] * df['S_SGC_DV1']**2 / df['S_SGSQ_1']), 0.01))

    os_sg.update(df.groupby(['ch_nom_1'])['S_N_SG_CH1'].agg("mean").to_dict())
    os_mu.update(df.groupby(['ch_nom_1'])['S_N_MU_CH1'].agg("mean").to_dict())

    to_drop = [c for c in df.columns if c.startswith('S_')]
    df.drop(to_drop, axis=1, inplace=True)
    return df.reset_index(drop=True)

def calc_oskill(df):
  os_sg = {}
  os_mu = {}
  df['win'] = (np.sign(df.ch_ordreArrivee_2 - df.ch_ordreArrivee_1) + 1.0) / 2.0
  bycr = df.groupby('aid_cr')
  r = bycr.apply(lambda x: calc_oskill_bycr(x,os_sg,os_mu))
  return r


