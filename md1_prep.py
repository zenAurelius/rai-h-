import pandas as pd
import numpy as np
import datetime

###############################################################################
class md1Preparator :

	def load_data(self, filename) :
		print("LOADING DATA...")
		datas = pd.read_csv(filename)
		print(datas.describe())
		return datas
		
	def orderedValue(self, row, courses, col_names) :	
		to_return = []
		for col_name in col_names :
			min, max = courses.get_group(row.REFERENCE)[col_name].agg(['min', 'max'])
			val = 0
			if(max - min > 0) :
				val = 2 * ((row[col_name] - min) / (max - min)) -1
			to_return.append(val)
		return to_return

	def extract_features(self, datas) :

		print('EXTRACT CATEGORICAL FEATURES...') #-------------------------------------------------
		self.dataset = datas[['LIEUX', 'DISTANCE', 'PRIX', 'SEXE_CHEVAL', 'SEASON']].copy()
		self.dataset.loc[:,'OEILLERE'] = datas['OEILLERE'].notna().astype(float)

		print('REFERENCE...') #--------------------------------------------------------------------
		self.dataset.loc[:,'REFERENCE'] = datas.REFERENCE
		
		print('GROUPING...') #---------------------------------------------------------------------
		print(datetime.datetime.now())
		courses = datas.groupby('REFERENCE')
		print(len(courses))
		print(datetime.datetime.now())
		col_names = ['NUM_PARTICIPATION', 'POIDS', 'CORDE', 'COTE']	
		ord_df = pd.DataFrame()
		for _, (u, rows) in enumerate(courses) :
			min = rows[col_names].min()
			max = rows[col_names].max()
			ord_df = ord_df.append(((rows[col_names] - min) / (max - min)).fillna(0))

		print(datetime.datetime.now())
		self.dataset[['NUM_0', 'POIDS_O', 'CORDE_O', 'COTE_O']] = ord_df
		print(datetime.datetime.now())
		print(self.dataset[['NUM_0', 'POIDS_O', 'CORDE_O', 'COTE_O']].describe())
		
		print('EXTRACT STANDARDIZE FEATURES...') #-------------------------------------------------
		self.dataset.loc[:,'TX_HIT_CO'] = ((datas['TX_HIT_CO'] - 0.085059) / 0.040525)
		self.dataset.loc[:,'LAST_WIN_CO'] = ((datas['LAST_WIN_CO'] - 21.502638) / 26.591206)
		self.dataset.loc[:,'NB_CO_DAY'] = ((datas['NB_CO_DAY'] - 3.455960) / 1.966135)
		self.dataset.loc[:,'NUM_CO_DAY'] = ((datas['NUM_CO_DAY'] - 2.244351) / 1.488554)
		self.dataset.loc[:,'HANDICAP'] = ((datas['HANDICAP'] - 2.816466) / 2.527261)
		self.dataset.loc[:,'AGE_CHEVAL'] = (((datas['AGE_CHEVAL'] - 1) / 4) - 1)
		print(datas[['NUM_CO_DAY', 'NB_CO_DAY', 'LAST_WIN_CO', 'TX_HIT_CO', 'HANDICAP', 'AGE_CHEVAL']].describe())
		print(self.dataset[['NUM_CO_DAY', 'NB_CO_DAY', 'LAST_WIN_CO', 'TX_HIT_CO', 'HANDICAP', 'AGE_CHEVAL']].describe())

	#**********************************************************************************************
	def add_target(self, datas)	:
		# ajoute les rapports 
		self.dataset[['RESULTAT', 'RPT_COUPLE', 'RPT_TRIO', 'RPT_TIERCEO', 'RPT_TIERCED', 'RPT_QUARTEO', 'RPT_QUARTED', 'RPT_QUINTEO', 'RPT_QUINTED']] = datas[['RESULTAT', 'RPT_COUPLE', 'RPT_TRIO', 'RPT_TIERCEO', 'RPT_TIERCED', 'RPT_QUARTEO', 'RPT_QUARTED', 'RPT_QUINTEO', 'RPT_QUINTED']]
		self.dataset['TARGET'] = datas.apply(lambda x : self.convertResultat(x), axis=1)
		self.dataset['COTE'] = datas['COTE']
		print(self.dataset[['RPT_COUPLE', 'RPT_TRIO', 'RPT_TIERCEO', 'RPT_TIERCED', 'RPT_QUARTEO', 'RPT_QUARTED', 'RPT_QUINTEO', 'RPT_QUINTED', 'TARGET']].describe())

	def convertResultat(self, row) :
		if row["RESULTAT"] == 1 :
			return 1.0
		elif row["RESULTAT"] == 2 : 
			return 0.5
		elif row["RESULTAT"] == 3 : 
			return 0.25
		elif row["RESULTAT"] == 4 : 
			return 0.125
		elif row["RESULTAT"] == 5 : 
			return 0.075
		else :
			return 0.0	

	def save_data(self, trainfile, devfile):


		train_set = pd.DataFrame()
		dev_set = pd.DataFrame()
		#groupe par reference
		self.dataset = self.dataset.reindex(np.random.permutation(self.dataset.index)).reset_index(drop=True)
		courses = self.dataset.groupby('REFERENCE', sort=False)
		
		full_size = len(courses)
		dev_size = int(self.devPercentage * full_size / 100)
		train_size = full_size - dev_size
		print(full_size)
		for i, (_, rows) in enumerate(courses) :
			if i < train_size :
				train_set = train_set.append(rows)
			else :
				dev_set = dev_set.append(rows)
				
		print("Train size = " + str(train_size))
		print(train_set.describe())
		print("Dev size = " + str(dev_size))
		print(dev_set.describe())
		
		train_set.to_csv(trainfile, index=False)
		dev_set.to_csv(devfile, index=False)
		

	def prepare_training(self, filename, trainset_file, devset_file):
		self.parameters = pd.DataFrame()
		self.devPercentage = 30
		datas = self.load_data(filename)
		self.extract_features(datas)
		self.add_target(datas)

		self.save_data(trainset_file, devset_file)
		


###############################################################################
prep = md1Preparator()
prep.prepare_training('./data/plat_2016_16.csv', './data/train.hrd', './data/dev.hrd')