import pandas as pd
import numpy as np
import datetime

import md_utility

###############################################################################
class md1Preparator :

	#----------------------------------------------------------------------------------------------
	def load_data(self, filename) :
		print("LOADING DATA...")
		datas = pd.read_csv(filename)
		print(datas.describe())
		return datas
		
	#----------------------------------------------------------------------------------------------
	def orderedValue(self, row, courses, col_names) :	
		to_return = []
		for col_name in col_names :
			min, max = courses.get_group(row.REFERENCE)[col_name].agg(['min', 'max'])
			val = 0
			if(max - min > 0) :
				val = 2 * ((row[col_name] - min) / (max - min)) -1
			to_return.append(val)
		return to_return

	#----------------------------------------------------------------------------------------------
	def extract_course_datas(self, course) :
		cat_lieux = ['DEAUVILLE', 'PORNICHET LA BAULE', 'CHANTILLY', 'SAINT CLOUD', 'CAGNES SUR MER', 'MAISONS LAFFITTE']
		first_course = course.iloc[0]

		datas = pd.DataFrame()
		datas['LIEUX'] = course.LIEUX.apply(lambda l : l if l in cat_lieux else 'AUTRE')
		datas['P_MAL'] = len(course[course.SEXE_CHEVAL == 'M']) / first_course.NB_PARTANT
		datas['P_FEM'] = len(course[course.SEXE_CHEVAL == 'F']) / first_course.NB_PARTANT
		datas['R_HEURE'] = first_course.HEURE[:2]
		datas['M_POIDS'] = course.POIDS.mean()
		datas['S_POIDS'] = course.POIDS.std()
		datas['M_AGE_CHEVAL'] = course.AGE_CHEVAL.mean()
		datas['S_AGE_CHEVAL'] = course.AGE_CHEVAL.std()
		datas['M_HANDICAP'] = course.HANDICAP.mean()
		datas['S_HANDICAP'] = course.HANDICAP.std()
		datas['SEASON'] = md_utility.convert_season(first_course.DATE_COURSE[5:7])

		# ordered features :
		of_names = ['POIDS', 'CORDE', 'NUM_PARTICIPATION', 'HANDICAP', 'AGE_CHEVAL']	
		for of in of_names :
			min_of = course[of].min()
			max_of = course[of].max()
			datas['O_' + of] = ((course[of] - min_of) / (max_of - min_of)).fillna(0)

		return datas

	#----------------------------------------------------------------------------------------------
	def extract_features(self, datas) :

		print(datetime.datetime.now(), '- EXTRACT RAW DATA...') #-----------------------------------------------------
		self.dataset = datas[['NUM_PARTICIPATION', 'RESULTAT_COURSE', 'DISTANCE', 'PRIX', 'SEXE_CHEVAL']]
		print(self.dataset)

		print(datetime.datetime.now(), '- EXTRACT DECODE PARTICIPATION FEATURES...') #-------------------------------------------------
		self.dataset['OEILLERE'] = datas['OEILLERE'].notna().astype(float)
		
		print(datetime.datetime.now(), '- GROUPING...') #---------------------------------------------------------------------
		courses = datas.groupby('REFERENCE')
		print(datetime.datetime.now(), '- NB COURSES = ', len(courses))
		print(datetime.datetime.now(), '- EXTRACT COURSE FEATURES = ', len(courses))
		self.dataset = pd.concat([self.dataset, courses.apply(lambda c : self.extract_course_datas(c)).reset_index(level=0)], axis=1)
		print(datetime.datetime.now(), '- COURSES FEATURES : ')
		print(self.dataset)
				
		print(datetime.datetime.now(), '- EXTRACT STANDARDIZE FEATURES...') #-------------------------------------------------
		print(datas[['AGE_CHEVAL', 'HANDICAP']].describe())

	#----------------------------------------------------------------------------------------------
	def add_target(self, datas)	:
		# ajoute les rapports 
		self.dataset[['RPT_COUPLE', 'RPT_TRIO', 'RPT_TIERCEO', 'RPT_TIERCED', 'RPT_QUARTEO', 'RPT_QUARTED', 'RPT_QUINTEO', 'RPT_QUINTED']] = datas[['RPT_COUPLE', 'RPT_TRIO', 'RPT_TIERCEO', 'RPT_TIERCED', 'RPT_QUARTEO', 'RPT_QUARTED', 'RPT_QUINTEO', 'RPT_QUINTED']]
		self.dataset['TARGET'] = datas.apply(lambda x : self.convertResultat(x), axis=1)
		self.dataset['COTE'] = datas['COTE']
		print(self.dataset[['RPT_COUPLE', 'RPT_TRIO', 'RPT_TIERCEO', 'RPT_TIERCED', 'RPT_QUARTEO', 'RPT_QUARTED', 'RPT_QUINTEO', 'RPT_QUINTED', 'TARGET']].describe())

	#----------------------------------------------------------------------------------------------
	def convertResultat(self, row) :
		if row["RESULTAT"] == 1 :
			return 1.0
		if row["RESULTAT"] == 2 : 
			return 1.0
		if row["RESULTAT"] == 3 : 
			return 1.0
		if row["RESULTAT"] == 4 : 
			return 0.0
		if row["RESULTAT"] == 5 : 
			return 0.0
		return 0.0	

	#----------------------------------------------------------------------------------------------
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

		# balancing train set :
		print('balancing...')
		counts = train_set["TARGET"].value_counts()
		print('counts before :\n',counts)
		df_loss = train_set[train_set["TARGET"] == 0]
		df_win = train_set[train_set["TARGET"] != 0]
		df_loss = df_loss.sample(counts.iloc[1])
		train_set = pd.concat([df_loss, df_win], axis=0)
		counts = train_set["TARGET"].value_counts()
		print('counts after : \n',counts)

		
		train_set.to_csv(trainfile, index=False)
		dev_set.to_csv(devfile, index=False)

	#----------------------------------------------------------------------------------------------
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