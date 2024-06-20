import pandas as pd

'''df = pd.read_csv('./data/volcania_p.csv')
df =df[['aid_cr', 'ch_nom_1', 'ch_driver_1', 'ch_ordreArrivee_1', 'ch_nom_2', 'ch_driver_2', 'ch_ordreArrivee_2']]
df.to_csv('./data/volcania_s.csv', index=False)'''

df = pd.read_csv('./data/volcania_s.csv')

params= {'tau':float(25.0 / 300.0), 'beta':float(25.0 / 6.0)}
b_sg = {}
b_mu = {}

df['S_SG_CH1'] = df.ch_nom_1.astype(str).map(b_sg).fillna(25)
df['S_SG_CH2'] = df.ch_nom_1.astype(str).map(b_sg).fillna(25) 
df['S_SG_DV1'] = df.ch_driver_1.astype(str).map(b_sg).fillna(25) 
df['S_SG_DV2'] = df.ch_driver_1.astype(str).map(b_sg).fillna(25)

df['S_MU_CH1'] = df.ch_nom_2.astype(str).map(b_sg).fillna(25)
df['S_MU_CH2'] = df.ch_nom_2.astype(str).map(b_sg).fillna(25) 
df['S_MU_DV1'] = df.ch_driver_2.astype(str).map(b_sg).fillna(25) 
df['S_MU_DV2'] = df.ch_driver_2.astype(str).map(b_sg).fillna(25) 

tsq = params.get('tau') * params.get('tau')
df['S_SGSQ_CH1'] = df['S_SG_CH1'] * df['S_SG_CH1'] + tsq
df['S_SGSQ_CH2'] = df['S_SG_CH2'] * df['S_SG_CH2'] + tsq
df['S_SGSQ_DV1'] = df['S_SG_DV1'] * df['S_SG_DV1'] + tsq
df['S_SGSQ_DV2'] = df['S_SG_DV2'] * df['S_SG_DV2'] + tsq

df['S_SGSQ_1'] = df['S_SG_CH1'] * df['S_SG_CH1'] + df['S_SG_DV1'] * df['S_SG_DV1'] 
df['S_SGSQ_2'] = df['S_SG_CH2'] * df['S_SG_CH2'] + df['S_SG_DV2'] * df['S_SG_DV2']
df['S_MU_1'] = df['S_MU_CH1'] + df['S_MU_DV1']
df['S_MU_2'] = df['S_MU_CH2'] + df['S_MU_DV2']

print(df.head())