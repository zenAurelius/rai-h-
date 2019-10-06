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

    #----------------------------------------------------------------------------------------------
    def extract_nth(self, x, col_name, pos) :
        xsorted = x.sort_values(col_name, ascending=True)
        return xsorted.iloc[pos]

    #----------------------------------------------------------------------------------------------
    def extract_ispos(self, x):
        list_pos = []
        list_pos.append(1 if x['RESULTAT'] == 1 else 0)
        list_pos.append(1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] <= 2) else 0)
        list_pos.append(1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] <= 3) else 0)
        return list_pos

    #----------------------------------------------------------------------------------------------
    def extract_features(self, datas) :
        # un enregistrement par course
        print(datetime.datetime.now(), "- GROUPING RACE...")
        courses = datas.groupby('REFERENCE')
        print(datetime.datetime.now(), "- GROUPING RACE... done")
        print(datetime.datetime.now(), len(courses))

        self.datas = pd.DataFrame(columns=['LIEUX'])
        self.datas.LIEUX = courses.first().LIEUX.apply(lambda x: self.lieux.index(x) / self.nb_lieux)
        self.datas['NB_PARTANT'] = courses.first().NB_PARTANT
        
        fav = courses.apply(lambda x : self.extract_nth(x, 'COTE', 0))[['NUM_PARTICIPATION', 'RESULTAT', 'RESULTAT_COURSE']]
        fav['TARGET'] = fav.apply(lambda x: 1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] <= 2) else 0, axis=1)
        self.datas[['FAV1', 'TARGET1']] = fav[['NUM_PARTICIPATION', 'TARGET']]
        
        sfav = courses.apply(lambda x : self.extract_nth(x, 'COTE', 1))[['NUM_PARTICIPATION', 'RESULTAT']]
        sfav['TARGET'] = sfav.apply(lambda x: 1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] <= 2) else 0, axis=1)
        self.datas[['FAV2', 'TARGET2']] = sfav[['NUM_PARTICIPATION', 'TARGET']]

        tfav = courses.apply(lambda x : self.extract_nth(x, 'COTE', 2))[['NUM_PARTICIPATION', 'RESULTAT']]
        tfav['TARGET'] = tfav.apply(lambda x: 1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] <= 2) else 0, axis=1)
        self.datas[['FAV3', 'TARGET3']] = tfav[['NUM_PARTICIPATION', 'TARGET']]
        
        #print(sfav)
        #print(pd.concat([self.datas, sfav], axis=1, sort=False))

        self.datas['TARGETA'] = self.datas.TARGET1
        self.datas['TARGETB'] = self.datas.TARGET1 | self.datas.TARGET2
        self.datas['TARGETC'] = self.datas.TARGET1 | self.datas.TARGET2 | self.datas.TARGET3
       
        cote = datas[datas.RESULTAT == 1][['REFERENCE', 'COTE']]
        self.datas['COTE'] = (cote.set_index('REFERENCE'))
        self.datas['TARGET'] = self.datas.apply( lambda x: 1 if x['COTE'] > 8.8 else 0, axis=1)
        print(self.datas)
        #print(self.datas.describe())
        print(self.datas.TARGETA.value_counts())
        print(self.datas.TARGETB.value_counts())
        print(self.datas.TARGETC.value_counts())

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