
import pandas as pd
import numpy as np

###############################################################################
class Enrichisseur:


	def enrichiCO(self, row):
		allOfCo = self.df[(self.df.CONDUCTEUR == row.CONDUCTEUR)]
		pastOfCo = allOfCo[allOfCo.REFERENCE < row.REFERENCE]
		lastWin = np.flatnonzero(pastOfCo['RESULTAT'] == 1)
		last_win_co = 100
		if(len(lastWin) > 0) :
			last_win_co = lastWin[0] + 1
			
		sameDaySameCo = allOfCo[allOfCo.DATE_COURSE == row.DATE_COURSE]
		nbToAdd = sameDaySameCo.shape[0]
		indices = np.flatnonzero(sameDaySameCo['REFERENCE'] == row.REFERENCE)
		
		allWinOfCo = allOfCo[allOfCo.RESULTAT == 1]
		if (len(allOfCo) > 0) :
			hit_co = len(allWinOfCo) / len(allOfCo)
		else :
			hit_co = 0.0
		
		print("{0} - {1} : {2}".format(self.nbTreated, nbToAdd, indices), end='\r')
		self.nbTreated += 1
		
		num_co_day = 0
		if(len(indices) > 0) :
			num_co_day = indices[0] + 1
			
		
			
		return [num_co_day, nbToAdd, last_win_co, hit_co]
		

	def run(self):
		#full = pd.read_csv('./data/full.csv')
		#self.df = full[full.TYPE_COURSE == 'p']
		#self.df.to_csv('./data/plat.csv', index=False)
		
		self.df = pd.read_csv('./data/plat.csv')
		
		self.df_2017 = self.df[(self.df.DATE_COURSE >= '2017-01-01') & (self.df.DATE_COURSE <= '2017-12-31') & (self.df.CONDUCTEUR.notna())].sort_values("REFERENCE", ascending=True)
		print(self.df_2017.describe())
		
		''' # ENRICHISSEMENT DE SEASON
		self.df['SEASON'] = pd.Series(self.df.DATE_COURSE.str.split('-', expand=True)[1], dtype='int64').mod(12).floordiv(3)
		print(self.df['SEASON'].describe())
		self.df.to_csv('./data/plat.csv', index=False)
		'''

		'''# ENRICHISSEMENT CO SUR 2017
		self.nbTreated = 0
		self.df_2017[["NUM_CO_DAY", "NB_CO_DAY", "LAST_WIN_CO", "TX_HIT_CO"]] = self.df_2017.apply(lambda x : self.enrichiCO(x), axis=1, result_type='expand')
		print(self.df_2017[["NUM_CO_DAY", "NB_CO_DAY", "LAST_WIN_CO", "TX_HIT_CO"]].describe())
		self.df_2017.to_csv('./data/plat_2017.csv', index=False)
		'''
		
		self.df_2014 = self.df[(self.df.DATE_COURSE >= '2014-01-01') & (self.df.DATE_COURSE <= '2014-12-31') & (self.df.CONDUCTEUR.notna())].sort_values("REFERENCE", ascending=True)
		print(self.df_2014.describe())
		self.nbTreated = 0
		self.df_2014[["NUM_CO_DAY", "NB_CO_DAY", "LAST_WIN_CO", "TX_HIT_CO"]] = self.df_2014.apply(lambda x : self.enrichiCO(x), axis=1, result_type='expand')
		print(self.df_2014[["NUM_CO_DAY", "NB_CO_DAY", "LAST_WIN_CO", "TX_HIT_CO"]].describe())
		self.df_2014.to_csv('./data/plat_2014.csv', index=False)
		
		
		''' # ENRICHISSEMENT CO SUR 2017_16
		self.df_16 = self.df_2017[(self.df_2017.NB_PARTANT == 16)]
		print(self.df_16.describe())
		self.nbTreated = 0
		self.df_16[["NUM_CO_DAY", "NB_CO_DAY", "LAST_WIN_CO", "TX_HIT_CO"]] = self.df_16.apply(lambda x : self.enrichi(x), axis=1, result_type='expand')
		print(self.df_16[["NUM_CO_DAY", "NB_CO_DAY", "LAST_WIN_CO", "TX_HIT_CO"]].describe())
		self.df_16.to_csv('./data/plat_2017_16.csv', index=False)
		'''

###############################################################################		
enr = Enrichisseur()
enr.run()