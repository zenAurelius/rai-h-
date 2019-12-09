import pandas as pd

def checkResultat(c):
    deux = c[c.RESULTAT == 2]
    if(len(deux) == 0) :
        print(c[['REFERENCE', 'RESULTAT', 'RESULTAT_COURSE', 'NUM_PARTICIPATION']])

lieux = ['DEAUVILLE','CHANTILLY','SAINT CLOUD','MAISONS LAFFITTE','LONGCHAMP','CAGNES SUR MER','MARSEILLE VIVAUX','COMPIEGNE','VICHY','TOULOUSE','LYON PARILLY','CLAIREFONTAINE','FONTAINEBLEAU','LA TESTE DE BUCH','LYON LA SOIE','MARSEILLE BORELY','PAU','PORNICHET LA BAULE','MONS','BORDEAUX LE BOUSCAT','LE CROISE LAROCHE','NANTES','KRANJI','NANCY','STRASBOURG','LE LION D ANGERS','ANGERS','AVENCHES','DEAUVILLE MIDI','AMIENS','SALON DE PROVENCE','MONT DE MARSAN','DAX','CHATEAUBRIANT','DIEPPE','ARGENTAN','CRAON','MOULINS','SAINT MALO','LE MANS','LES SABLES D''OLONNE','AIX LES BAINS','TARBES','LION D''ANGERS','CHOLET','LES SABLES','VITTEL','EVREUX','SENONNES','CARRERE','NIMES','CAVAILLON','AGEN','LIGNIERES','LE TOUQUET','ANGOULEME','MORLAIX','MACHECOUL','CARPENTRAS','VICHY SOIR','POMPADOUR','ROYAN LA PALMYRE','LA ROCHE POSAY','AUTEUIL','CHAMP DE MARS','NORT SUR ERDRE','SAINT MORITZ','PAU MIDI','HYERES','TOURS','AJACCIO','AVENCHES SOIR','MONTLUCON NERIS','CHAMPS DE MARS','DIVONNE LES BAINS','SABLE SUR SARTHE','CAGNES MIDI','BLAIN']

#datas = pd.read_csv("./data/plat.csv", index_col='ID')
datas = pd.read_csv("./data/resultats.csv", index_col='REFERENCE')
new_datas = datas[['RESULTAT_COURSE','COTE']]
new_datas['RPT_CO'] = datas.RPT_COUPLE / 1.5
new_datas['RPT_TO'] = datas.RPT_TRIO / 1.5
new_datas['RPT_TI_O'] = datas.RPT_QUARTEO
new_datas['RPT_TI_D'] = datas.RPT_QUARTED
new_datas['RPT_QA_O'] = datas.RPT_QUINTEO / 1.3
new_datas['RPT_QA_D'] = datas.RPT_QUINTED / 1.3
new_datas['RPT_QI_O'] = datas.RPT_TIERCEO / 2
new_datas['RPT_QI_D'] = datas.RPT_TIERCED / 2
print(new_datas)
new_datas.to_csv('./data/resultats_clean.csv')
#print(datas.iloc[:,[29,31]])
#selection des premiers de chaque course
'''indexNames = datas[ datas['RESULTAT'] != 1 ].index
datas.drop(indexNames , inplace=True)
datas = datas[['REFERENCE','RESULTAT_COURSE','COTE','RPT_COUPLE','RPT_TRIO','RPT_TIERCEO','RPT_TIERCED','RPT_QUARTEO','RPT_QUARTED','RPT_QUINTEO','RPT_QUINTED']]
datas.set_index('REFERENCE', inplace=True)
print(len(datas))
print(datas)
datas.to_csv('./data/resultats.csv')'''

#datas = datas[datas.LIEUX.isin(lieux)]
#indexNames = datas[ datas['RESULTAT_COURSE'].isna() ].index
#datas.drop(indexNames , inplace=True)
#datas.to_csv('./data/plat_enr2.csv')
#print(len(datas))


#by_cr = datas.groupby('REFERENCE')
#by_cr.apply(lambda c : checkResultat(c))

#print(datas.RESULTAT.value_counts())

#datas = datas.drop(columns=['CONDUCTEUR.1'])
#datas.CONDUCTEUR.value_counts().to_csv('./data/check.csv')