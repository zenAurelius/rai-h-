import pandas as pd
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
		print('EXTRACT CATEGORICAL FEATURES...')
		self.dataset = datas[['LIEUX', 'DISTANCE', 'PRIX', 'SEXE_CHEVAL', 'SEASON']].copy()
		self.dataset.loc[:,'OEILLERE'] = datas['OEILLERE'].notna().astype(float)
		
		print('GROUPING...')
		print(datetime.datetime.now())
		courses = datas.groupby('REFERENCE')
		print(len(courses))
		print(datetime.datetime.now())
		col_names = ['NUM_PARTICIPATION', 'POIDS', 'CORDE', 'COTE']	
		ord_df = pd.DataFrame()
		for i, (u, rows) in enumerate(courses) :
			min = rows[col_names].min()
			max = rows[col_names].max()
			ord_df = ord_df.append((rows[col_names] - min) / (max - min))
		print(datetime.datetime.now())
		self.dataset[['NUM_0', 'POIDS_O', 'CORDE_O', 'COTE_O']] = ord_df
		print(datetime.datetime.now())
		print(self.dataset[['NUM_0', 'POIDS_O', 'CORDE_O', 'COTE_O']].describe())
		
		print('EXTRACT STANDARDIZE FEATURES...')
		self.dataset.loc[:,'TX_HIT_CO'] = ((datas['TX_HIT_CO'] - 0.085059) / 0.040525)
		self.dataset.loc[:,'LAST_WIN_CO'] = ((datas['LAST_WIN_CO'] - 21.502638) / 26.591206)
		self.dataset.loc[:,'NB_CO_DAY'] = ((datas['NB_CO_DAY'] - 3.455960) / 1.966135)
		self.dataset.loc[:,'NUM_CO_DAY'] = ((datas['NUM_CO_DAY'] - 2.244351) / 1.488554)
		self.dataset.loc[:,'HANDICAP'] = ((datas['HANDICAP'] - 2.816466) / 2.527261)
		self.dataset.loc[:,'AGE_CHEVAL'] = (((datas['AGE_CHEVAL'] - 1) / 4) - 1)
		print(datas[['NUM_CO_DAY', 'NB_CO_DAY', 'LAST_WIN_CO', 'TX_HIT_CO', 'HANDICAP', 'AGE_CHEVAL']].describe())
		print(self.dataset[['NUM_CO_DAY', 'NB_CO_DAY', 'LAST_WIN_CO', 'TX_HIT_CO', 'HANDICAP', 'AGE_CHEVAL']].describe())

	def add_target(self, datas)	:
		# ajoute les rapports 
		self.dataset[['RPT_COUPLE', 'RPT_TRIO', 'RPT_TIERCEO', 'RPT_TIERCED', 'RPT_QUARTEO', 'RPT_QUARTED', 'RPT_QUINTEO', 'RPT_QUINTED']] = datas[['RPT_COUPLE', 'RPT_TRIO', 'RPT_TIERCEO', 'RPT_TIERCED', 'RPT_QUARTEO', 'RPT_QUARTED', 'RPT_QUINTEO', 'RPT_QUINTED']]
		print(self.dataset[['RPT_COUPLE', 'RPT_TRIO', 'RPT_TIERCEO', 'RPT_TIERCED', 'RPT_QUARTEO', 'RPT_QUARTED', 'RPT_QUINTEO', 'RPT_QUINTED']].describe())
		
	def prepare_training(self, filename, file_to_save):
		self.parameters = pd.DataFrame()
		datas = self.load_data(filename)
		self.extract_features(datas)
		self.add_target(datas)

		self.dataset.to_csv(file_to_save, index=False)


###############################################################################
prep = md1Preparator()
prep.prepare_training('./data/plat_2017_16.csv', './data/prep.csv')