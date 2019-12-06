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
        self.cr_data = ['REFERENCE','RESULTAT','RESULTAT_COURSE','NUM_PARTICIPATION']
        self.cr_features = ['LIEUX','REUNION','DISTANCE','PRIX','NB_PARTANT','HEURE','NUM_COURSE','SEASON','P_MAL','P_FEM','M_POIDS','S_POIDS','M_AGE_CHEVAL','S_AGE_CHEVAL']
        self.ch_features = ['SEXE_CHEVAL','AGE_CHEVAL','POIDS','CORDE','HANDICAP']
        self.co_features = ['CO_LAST_WIN','CO_TX_HIT','CO_KNOWN_CR','CO_NB_INDAY','CO_NUM_INDAY']
        self.all_features = self.cr_features + self.ch_features + self.co_features
        self.p1_features = [f + '_P1' for f in (self.ch_features + self.co_features)]
        self.p2_features = [f + '_P2' for f in (self.ch_features + self.co_features)]

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
    def add_comparaison(self, p, o) :
        new_data = []
        for f in (self.co_features + self.ch_features) :
            new_data.add(p[f])
            #new_data[f +'_P2'] = o[f]
        #for f in self.cr_features :
        #    new_data[f] = p[f]'''
        if p.RESULTAT != 0 and (o.RESULTAT == 0 or (p.RESULTAT < o.RESULTAT)) :
            new_data.add(1)
        else :
            new_data.add(0)
        #print(p.RESULTAT, o.RESULTAT, new_data.TARGET)
        return new_data

    #----------------------------------------------------------------------------------------------
    def extract_1c1(self, p, others) :
        df1 = others.apply(lambda o : self.add_comparaison(p,o), axis=1)
        #df2 = others.apply(lambda o : self.add_comparaison(o,p), axis=1)
        #self.dev_set = pd.concat([self.dev_set, df1, df2])
        return df1

    #----------------------------------------------------------------------------------------------
    def traite_course(self, course) :
        print("course")
        arrives = course[course.RESULTAT > 0]
        print(arrives)
        result = arrives.apply(lambda p : self.extract_1c1(p, course[course.NUM_PARTICIPATION != p.NUM_PARTICIPATION]), axis=1)
        print(result)
        return result

    #----------------------------------------------------------------------------------------------
    def split_features(self, courses) :
        self.dev_set = pd.DataFrame()
        full_size = len(courses)
        dev_size = int(self.dev_percentage * full_size / 100)
        print('sizes : ', full_size, dev_size)
        
        courses.apply(lambda c : self.traite_course(c))
        
        [self.traite_course(i, g[1]) for i,g in enumerate(list(courses)[:dev_size])]
        #train_list = [g[1] for g in list(courses)[dev_size:]]
        #dev_set = pd.concat(dev_list)
        #train_set = pd.concat(train_list)
        print(self.dev_set)
        #print(train_set.describe())

    #----------------------------------------------------------------------------------------------
    def add_target(self, datas) :
        self.datas['TARGET'] = 0
        print(self.datas)

    #----------------------------------------------------------------------------------------------
    def prepare_training(self, filename, trainset_file, devset_file):
        self.parameters = pd.DataFrame()
        self.dev_percentage = 3

        datas = super().load_data(filename)
        datas = datas[(datas.DATE_COURSE > '2013-12-31') & (datas.DATE_COURSE < '2016-12-31')]
        print('selected datas : ', len(datas))

        # sélection des features parmi les données
        features = self.extract_features(datas)
        
        # traitement par course : groupe, split, transforme en 1c1
        print('- group by REFERENCE...')
        features = features.reindex(np.random.permutation(features.index)).reset_index(drop=True)
        courses = features.groupby('REFERENCE', sort=False)
        print('- group by REFERENCE...done : ', len(courses))
        
        self.split_features(courses)
        #self.save_data(trainset_file, devset_file)

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

ext = co1c1Extract()
ext.prepare_training('./data/plat.csv', './data/train2.hrd', './data/dev2.hrd')