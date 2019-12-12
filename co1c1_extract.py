import pandas as pd
import numpy as np
import datetime

from hrai_extract import hraiExtract

###################################################################################################
# co1c1_extract : on extrait des données co, on les splits, on transforme en 1c1
###################################################################################################
class co1c1Extract(hraiExtract) :

    #----------------------------------------------------------------------------------------------
    def __init__(self) :
        super().__init__()
        self.cr_data = ['RESULTAT','RESULTAT_COURSE','NUM_PARTICIPATION']
        self.cr_features = ['REFERENCE','LIEUX','REUNION','DISTANCE','PRIX','NB_PARTANT','HEURE','NUM_COURSE','SEASON','P_MAL','P_FEM','M_POIDS','S_POIDS','M_AGE_CHEVAL','S_AGE_CHEVAL']
        self.ch_features = ['SEXE_CHEVAL','AGE_CHEVAL','POIDS','CORDE','HANDICAP']
        self.co_features = ['CO_LAST_WIN','CO_TX_HIT','CO_KNOWN_CR','CO_NB_INDAY','CO_NUM_INDAY']
        self.all_features = self.cr_features + self.ch_features + self.co_features

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
        
        features_names = self.cr_features + self.ch_features + self.co_features + self.cr_data
        features = datas[features_names]
        # modifie des features
        cat_lieux = ['DEAUVILLE', 'PORNICHET LA BAULE', 'CHANTILLY', 'SAINT CLOUD', 'CAGNES SUR MER', 'MAISONS LAFFITTE']
        features.LIEUX = features.LIEUX.apply(lambda l : l if l in cat_lieux else 'AUTRE')
        features.HEURE = features.HEURE.str[:2]

        return features

    #----------------------------------------------------------------------------------------------
    def extract_1c1(self, p, o) :
        #print(p)
        p1 = pd.Series(p[self.all_features]).rename(lambda i : i + '_P1')
        p2 = pd.Series(o[self.all_features]).rename(lambda i : i + '_P2')
        new_data = pd.concat([p1,p2])
        new_data['TARGET'] = p.RESULTAT != 0 and (o.RESULTAT == 0 or (p.RESULTAT < o.RESULTAT))
        #print(new_data)
        return new_data

    #----------------------------------------------------------------------------------------------
    def traite_course(self, course, dev_size) :
        print(datetime.datetime.now(), 'c', self.nbC, end='\r')
        print(course)
        self.nbC += 1
        arrives = course[course.RESULTAT > 0]
        result = []
        for i in range(len(arrives)) :
            a = arrives.iloc[i]
            others = course[course.NUM_PARTICIPATION != a.NUM_PARTICIPATION]
            result.append(others.apply(lambda o : self.extract_1c1(a, o), axis=1))
            result.append(others.apply(lambda o : self.extract_1c1(o, a), axis=1))
        full1 = pd.concat(result)
        print(full1)
        if self.nbC < dev_size :
            self.dev_list.append(full1)
        else :
            self.train_list.append(full1)

    #----------------------------------------------------------------------------------------------
    def split_features(self, courses) :
        self.dev_list = []
        self.train_list = []
        full_size = len(courses)
        dev_size = int(self.dev_percentage * full_size / 100)
        print('sizes : ', full_size, dev_size)
        self.nbC = 0
        courses.apply(lambda c : self.traite_course(c, dev_size))
        self.dev_set = pd.concat(self.dev_list)
        self.train_set = pd.concat(self.train_list)

    #----------------------------------------------------------------------------------------------
    def add_target(self, datas) :
        self.datas['TARGET'] = 0
        print(self.datas)

    #----------------------------------------------------------------------------------------------
    def prepare_training(self, filename, trainset_file, devset_file):
        self.parameters = pd.DataFrame()
        self.dev_percentage = 30

        datas = super().load_data(filename)
        datas = datas[(datas.DATE_COURSE > '2013-12-31') & (datas.DATE_COURSE < '2016-12-31')]
        print('selected datas : ', len(datas))

        # sélection des features parmi les données
        features = self.extract_features(datas)
        
        #features.to_csv('./data/filtered_features.csv')
        # traitement par course : groupe, split, transforme en 1c1
        print('- group by REFERENCE...')
        features = features.reindex(np.random.permutation(features.index)).reset_index(drop=True)
        print(features.head())
        courses = features.groupby('REFERENCE', sort=False)
        print('- group by REFERENCE...done : ', len(courses))
        
        self.split_features(courses)
        #self.save_data(trainset_file, devset_file)

    #----------------------------------------------------------------------------------------------
    def save_data(self, trainfile, devfile):

        print("Train size = " + str(len(self.train_set.index)))
        print(self.train_set.describe())
        print("Dev size = " + str(len(self.dev_set.index)))
        print(self.dev_set.describe())

        self.train_set.to_csv(trainfile)
        self.dev_set.to_csv(devfile)

###################################################################################################
###################################################################################################

ext = co1c1Extract()
ext.prepare_training('./data/plat.csv', './data/train2.hrd', './data/dev2.hrd')