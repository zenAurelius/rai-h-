import pandas as pd

def extract(x) :
    if x['NB_PARTANT'].iloc[0] > len(x) :
        x['NB_PARTANT'] = len(x)
    return x

datas = pd.read_csv("./data/plat_enr2s.csv")
#datas = datas.sort_values('REFERENCE')
#datas.to_csv('./data/plat_enr2s.csv', index=False)
print(datas[datas.NB_PARTANT == 64][['REFERENCE', 'NOM_CHEVAL', 'NUM_PARTICIPATION']])
#print(datas.NB_PARTANT.value_counts())

#datas.LIEUX.value_counts().to_csv('./data/plat_lieux.csv', index=True)
#dedoublon = datas.drop_duplicates(['REFERENCE', 'NUM_PARTICIPATION'])
#grouped = dedoublon.groupby('REFERENCE')
#ndf = grouped.apply(lambda x : extract(x))
#print(ndf.NB_PARTANT.value_counts())

#ndf.to_csv('./data/plat_enr3.csv', index=False)
