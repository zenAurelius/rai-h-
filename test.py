
import pandas as pd


def pct_place(df):
    pct = 100 * len(df[df.ch_ordreArrivee_1 <= 3.0]) / len(df)
    print(f'placé {pct}%')

df = pd.read_csv('./data/pmu2014_c_e.csv')
print(df.describe())
##df[df.ch_nom_1 == 'VALEUR DANOVER'].to_csv('test.csv')


result = result = df.groupby(['aid_cr', 'ch_nom_1']).first().reset_index()
result['Rang'] = result.groupby('aid_cr')['ELO_1'].rank(ascending=False)

pct_place(result[result.Rang == 1.0])
pct_place(result[result.Rang == 2.0])
pct_place(result[result.Rang == 3.0])
pct_place(result[result.Rang == 10.0])


