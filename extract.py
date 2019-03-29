
import pandas as pd
import numpy as np



class HraiExtractor:


	def calcNb(self, row):
		allOfCo = self.df[(self.df.CONDUCTEUR == row.CONDUCTEUR)]
		pastOfCo = allOfCo[allOfCo.REFERENCE < row.REFERENCE]
		lastWin = np.flatnonzero(pastOfCo['RESULTAT'] == 1)
		last_win_co = 100
		if(len(lastWin) > 0) :
			last_win_co = lastWin[0] + 1
			
		sameDaySameCo = allOfCo[allOfCo.DATE_COURSE == row.DATE_COURSE]
		nbToAdd = sameDaySameCo.shape[0]
		indices = np.flatnonzero(sameDaySameCo['REFERENCE'] == row.REFERENCE)
		#if(nbToAdd == 13) :
		#	print(row.REFERENCE)
		#	print(sameDaySameCo[['REFERENCE', 'NB_PARTANT']])
		
		#print(allOfCo[['REFERENCE', 'DATE_COURSE', 'CONDUCTEUR', 'RESULTAT']])
		#print(lastWin)

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
		self.df = pd.read_csv('./data/plat.csv', na_values = [''])
		print(self.df.iloc[:, 29:32])
		
		self.df_2017 = self.df[(self.df.DATE_COURSE >= '2017-01-01') & (self.df.DATE_COURSE <= '2017-12-31') & (self.df.CONDUCTEUR.notna())].sort_values("REFERENCE", ascending=True)
		print(self.df_2017.describe())
		
		self.df_16 = self.df_2017[(self.df_2017.NB_PARTANT == 16)]
		print(self.df_16.describe())
		
		#counts = self.df_16["CONDUCTEUR"].value_counts()
		#print(counts)
		
		#grouped = self.df_16.groupby(['DATE_COURSE'])
		#print(grouped.describe())
		#print(grouped)
		
		self.nbTreated = 0
		self.df_16[["NUM_CO_DAY", "NB_CO_DAY", "LAST_WIN_CO", "TX_HIT_CO"]] = self.df_16.apply(lambda x : self.calcNb(x), axis=1, result_type='expand')

		print(self.df_16[["NUM_CO_DAY", "NB_CO_DAY", "LAST_WIN_CO", "TX_HIT_CO"]].describe())
		self.df_16.to_csv('./data/plat_16.csv', index=False)
		
ext = HraiExtractor()
ext.run()