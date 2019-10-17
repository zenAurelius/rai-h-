import pandas as pd
import numpy as np
import datetime

###################################################################################################
# Modele 2 : Trouver c rentable ie 1er n'est pas le fav, ni le sfav ni le tfav et autre combinaison
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
        # il existe de partant à cote 0.0 => erreur ? en fait non partant ?, on les mets en fin de cote
        datas['COTE'] = datas['COTE'].apply(lambda x : x if x > 0 else 100)
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
    def convertSeason(self, x) :
        if x in ['12', '01', '02'] :
            return 0
        if x in ['03', '04', '05'] :
            return 1
        if x in ['06', '07', '08'] :
            return 2
        if x in ['09', '10', '11'] :
            return 3
        return 4 

    #----------------------------------------------------------------------------------------------
    def extractDatas(self, course) :
        cat_lieux = ['DEAUVILLE', 'PORNICHET LA BAULE', 'CHANTILLY', 'SAINT CLOUD', 'CAGNES SUR MER', 'MAISONS LAFFITTE']
        first_course = course.iloc[0]
        favoris = course[course.COTE < 8]
        
        datas = pd.DataFrame()
        datas['LIEUX'] = pd.Series(first_course.LIEUX if first_course.LIEUX in cat_lieux else 'AUTRE')
        datas['P_MAL'] = len(course[course.SEXE_CHEVAL == 'M']) / first_course.NB_PARTANT
        datas['P_FEM'] = len(course[course.SEXE_CHEVAL == 'F']) / first_course.NB_PARTANT
        datas['R_HEURE'] = first_course.HEURE[:2]
        datas['M_POIDS'] = course.POIDS.mean()
        datas['S_POIDS'] = course.POIDS.std()
        datas['M_AGE_CHEVAL'] = course.AGE_CHEVAL.mean()
        datas['S_AGE_CHEVAL'] = course.AGE_CHEVAL.std()
        datas['FM_POIDS'] = favoris.POIDS.mean()
        datas['FM_AGE_CHEVAL'] = favoris.AGE_CHEVAL.mean()
        datas['FP_MAL'] = len(favoris[favoris.SEXE_CHEVAL == 'M']) / len(favoris)
        datas['FP_FEM'] = len(favoris[favoris.SEXE_CHEVAL == 'F']) / len(favoris)
        datas['SEASON'] = self.convertSeason(first_course.DATE_COURSE[5:7])

        return datas
        
    #----------------------------------------------------------------------------------------------
    def extract_features(self, datas) :
        # un enregistrement par course
        print(datetime.datetime.now(), "- GROUPING RACE...")
        courses = datas.groupby('REFERENCE')
        print(datetime.datetime.now(), "- GROUPING RACE... done")
        print(datetime.datetime.now(), len(courses))

        print(datas.iloc[0].index)
        self.datas = pd.DataFrame()
        feature_named = ['DISTANCE', 'REUNION', 'PRIX', 'NUM_COURSE', 'NB_PARTANT', 'DATE_COURSE', 'HEURE']
        self.datas[feature_named] = courses.first()[feature_named]

        course_datas = courses.apply(lambda x : self.extractDatas(x))
        course_datas = course_datas.reset_index(level=1, drop=True)
        self.datas = pd.concat([self.datas, course_datas], axis=1)
        print(self.datas)
        
        fav1 = courses.apply(lambda x : self.extract_nth(x, 'COTE', 0))[['NUM_PARTICIPATION', 'RESULTAT', 'RESULTAT_COURSE', 'COTE']]
        fav1['TARGET'] = fav1.apply(lambda x: 1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] < 2) else 0, axis=1)
        self.datas[['FAV1', 'TARGET1', 'COTE1']] = fav1[['NUM_PARTICIPATION', 'TARGET', 'COTE']]
        
        fav2 = courses.apply(lambda x : self.extract_nth(x, 'COTE', 1))[['NUM_PARTICIPATION', 'RESULTAT', 'COTE']]
        fav2['TARGET'] = fav2.apply(lambda x: 1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] < 2) else 0, axis=1)
        self.datas[['FAV2', 'TARGET2', 'COTE2']] = fav2[['NUM_PARTICIPATION', 'TARGET', 'COTE']]

        fav3 = courses.apply(lambda x : self.extract_nth(x, 'COTE', 2))[['NUM_PARTICIPATION', 'RESULTAT', 'COTE']]
        fav3['TARGET'] = fav3.apply(lambda x: 1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] < 2) else 0, axis=1)
        self.datas[['FAV3', 'TARGET3', 'COTE3']] = fav3[['NUM_PARTICIPATION', 'TARGET', 'COTE']]

        fav4 = courses.apply(lambda x : self.extract_nth(x, 'COTE', 3))[['NUM_PARTICIPATION', 'RESULTAT', 'COTE']]
        fav4['TARGET'] = fav4.apply(lambda x: 1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] < 2) else 0, axis=1)
        self.datas[['FAV4', 'TARGET4', 'COTE4']] = fav4[['NUM_PARTICIPATION', 'TARGET', 'COTE']]

        fav5 = courses.apply(lambda x : self.extract_nth(x, 'COTE', 4))[['NUM_PARTICIPATION', 'RESULTAT', 'COTE']]
        fav5['TARGET'] = fav5.apply(lambda x: 1 if (x['RESULTAT'] >= 1 and x['RESULTAT'] < 2) else 0, axis=1)
        self.datas[['FAV5', 'TARGET5', 'COTE5']] = fav5[['NUM_PARTICIPATION', 'TARGET', 'COTE']]
        
        print(self.datas)
        #print(sfav)
        #print(pd.concat([self.datas, sfav], axis=1, sort=False))

        self.datas['TARGETA'] = self.datas.TARGET1
        self.datas['TARGETB'] = self.datas.TARGET1 | self.datas.TARGET2
        self.datas['TARGETC'] = self.datas.TARGET1 | self.datas.TARGET2 | self.datas.TARGET3
       
        gcote = datas[datas.RESULTAT == 1][['REFERENCE', 'COTE']]
        self.datas['GCOTE'] = (gcote.set_index('REFERENCE'))
        self.datas['TARGET'] = self.datas.apply( lambda x: 1 if x['GCOTE'] > 8.8 else 0, axis=1)
        print(self.datas)
        #print(self.datas.describe())

        print(self.datas.TARGETA.value_counts())
        print(self.datas.TARGETB.value_counts())
        print(self.datas.TARGETC.value_counts())

        print(self.datas.TARGET1.value_counts())
        print(self.datas.TARGET2.value_counts())
        print(self.datas.TARGET3.value_counts())
        print(self.datas.TARGET4.value_counts())
        print(self.datas.TARGET5.value_counts())

        print((self.datas['TARGET1'] * self.datas['COTE1']).sum())
        print((self.datas['TARGET2'] * self.datas['COTE2']).sum())
        print((self.datas['TARGET3'] * self.datas['COTE3']).sum())
        print((self.datas['TARGET4'] * self.datas['COTE4']).sum())
        print((self.datas['TARGET5'] * self.datas['COTE5']).sum())

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

        self.save_data(trainset_file, devset_file)

    #----------------------------------------------------------------------------------------------
    def save_data(self, trainfile, devfile):

        train_set = self.datas.sample(frac=0.75, random_state=0)
        dev_set = self.datas.drop(train_set.index)

        print("Train size = " + str(len(train_set.index)))
        print(train_set.describe())
        print("Dev size = " + str(len(dev_set.index)))
        print(dev_set.describe())

        train_set.to_csv(trainfile, index=False)
        dev_set.to_csv(devfile, index=False)

###################################################################################################
###################################################################################################

prep = md2Preparator()
prep.prepare_training('./data/plat_2016_16.csv', './data/train2.hrd', './data/dev2.hrd')