import pandas as pd
import numpy as np
import datetime

###################################################################################################
###################################################################################################
class md2Preparator :

    #----------------------------------------------------------------------------------------------
    def __init__(self) :
        self.lieux = ['DEAUVILLE','CHANTILLY','SAINT CLOUD','MAISONS LAFFITTE','LONGCHAMP','CAGNES SUR MER','MARSEILLE VIVAUX','COMPIEGNE','VICHY','TOULOUSE','LYON PARILLY','CLAIREFONTAINE','FONTAINEBLEAU','LA TESTE DE BUCH','LYON LA SOIE','MARSEILLE BORELY','PAU','PORNICHET LA BAULE','MONS','BORDEAUX LE BOUSCAT','LE CROISE LAROCHE','NANTES','KRANJI','NANCY','STRASBOURG','LE LION D ANGERS','ANGERS','AVENCHES','DEAUVILLE MIDI','AMIENS','SALON DE PROVENCE','MONT DE MARSAN','DAX','CHATEAUBRIANT','DIEPPE','ARGENTAN','CRAON','MOULINS','SAINT MALO','LE MANS','LES SABLES D''OLONNE','AIX LES BAINS','TARBES','LION D''ANGERS','CHOLET','LES SABLES','VITTEL','EVREUX','SENONNES','CARRERE','NIMES','CAVAILLON','AGEN','LIGNIERES','LE TOUQUET','ANGOULEME','MORLAIX','MACHECOUL','CARPENTRAS','VICHY SOIR','POMPADOUR','ROYAN LA PALMYRE','LA ROCHE POSAY','AUTEUIL','CHAMP DE MARS','NORT SUR ERDRE','SAINT MORITZ','PAU MIDI','HYERES','TOURS','AJACCIO','AVENCHES SOIR','MONTLUCON NERIS','CHAMPS DE MARS','DIVONNE LES BAINS','SABLE SUR SARTHE','CAGNES MIDI','BLAIN']
        self.nb_lieux = len(self.lieux)

    #----------------------------------------------------------------------------------------------
    def load_data(self, filename) :
        print("LOADING DATA...")
        datas = pd.read_csv(filename, index_col='ID')
        print("LOADING DATA...done")
        print(datas.describe())
        return datas

    def f(self, x) :
        xsorted = x.sort_values('COTE', ascending=True)
        return xsorted.iloc[1]
    #----------------------------------------------------------------------------------------------
    def extract_features(self, datas) :
        # un enregistrement par course
        print(datetime.datetime.now(), "- GROUPING RACE...")
        courses = datas.groupby('REFERENCE')
        print(datetime.datetime.now(), "- GROUPING RACE... done")
        print(datetime.datetime.now(), len(courses))

        self.datas = pd.DataFrame(columns=['LIEUX'])
        self.datas.LIEUX = courses.first().LIEUX.apply(lambda x: self.lieux.index(x) / self.nb_lieux)
        print(self.datas)

        fav = datas.loc[courses['COTE'].idxmin()][['REFERENCE', 'NUM_PARTICIPATION', 'RESULTAT']]
        fav['TARGET1'] = fav.apply(lambda x : 1 if x['RESULTAT'] == 1 else 0, axis=1)
        fav['TARGET2'] = fav.apply(lambda x : 1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] <= 2) else 0, axis=1)
        fav['TARGET3'] = fav.apply(lambda x : 1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] <= 3) else 0, axis=1)
        print(fav)
        print(fav.TARGET1.value_counts())
        print(fav.TARGET2.value_counts())
        print(fav.TARGET3.value_counts())

        sfav = courses.apply(self.f)[['NUM_PARTICIPATION', 'RESULTAT']]
        sfav['TARGET1'] = sfav.apply(lambda x : 1 if x['RESULTAT'] == 1 else 0, axis=1)
        sfav['TARGET2'] = sfav.apply(lambda x : 1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] <= 2) else 0, axis=1)
        sfav['TARGET3'] = sfav.apply(lambda x : 1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] <= 3) else 0, axis=1)
        print(sfav)
        print(sfav.TARGET1.value_counts())
        print(sfav.TARGET2.value_counts())
        print(sfav.TARGET3.value_counts())

        cote = datas[datas.RESULTAT == 1][['REFERENCE', 'COTE']]
        self.datas['COTE'] = (cote.set_index('REFERENCE'))
        self.datas['TARGET'] = self.datas.apply( lambda x: 1 if x['COTE'] > 8.8 else 0, axis=1)
        #print(self.datas)
        #print(self.datas.describe())
        #print(self.datas.TARGET.value_counts())

    #----------------------------------------------------------------------------------------------
    def add_target(self, datas) :
        self.datas['TARGET'] = 0
        print(self.datas)
    #----------------------------------------------------------------------------------------------
    def prepare_training(self, filename, trainset_file, devset_file):
        self.parameters = pd.DataFrame()
        self.devPercentage = 30

        datas = self.load_data(filename)
        self.extract_features(datas)
        #self.add_target(datas)

        #self.save_data(trainset_file, devset_file)

###################################################################################################
###################################################################################################

prep = md2Preparator()
prep.prepare_training('./data/plat_2016_16.csv', './data/train2.hrd', './data/dev2.hrd')