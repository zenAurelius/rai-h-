
import pandas as pd
import numpy as np
import datetime

###############################################################################
class Enrichisseur:


	def enr_co_1(self, group, row) :
		print(self.nbT, end='\r')
		self.nbT += 1
		
		idx = np.flatnonzero(group['REFERENCE'] == row.REFERENCE)
		nb_co_day = len(group)
		num_co_day = 0
		if(len(idx) > 0) :
			num_co_day = idx[0] + 1
		return [num_co_day, nb_co_day]
		
	def enr_co_0(self, group, row) :
		print(self.nbT, end='\r')
		self.nbT += 1
		pastOfCo = group[group.REFERENCE < row.REFERENCE].sort_values('REFERENCE', ascending=False)
		lastWin = np.flatnonzero(pastOfCo['RESULTAT'] == 1)
		last_win_co = 100
		if(len(lastWin) > 0) :
			last_win_co = lastWin[0] + 1
		return last_win_co
			

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
		
		# 0
		print(datetime.datetime.now())
		r = []
		coco = self.df.groupby('CONDUCTEUR')
		self.nbT = 0
		for i, (u, r_co) in enumerate(coco) :
			# 1
			col = r_co.apply(lambda x : self.enr_co_0(r_co, x), axis=1)
			r.append(r_co.assign(LAST_WIN_CO = col))
		self.df = pd.concat(r)
		
		# 1
		print(datetime.datetime.now())
		r = []
		coco = self.df.groupby('CONDUCTEUR')
		self.nbT = 0
		for i, (u, r_co) in enumerate(coco) :	
			sd_g_co = r_co.groupby('DATE_COURSE')
			for j, (_, sd_r_co) in enumerate(sd_g_co) :
				col = sd_r_co.apply(lambda x : self.enr_co_1(sd_r_co, x), axis=1, result_type='expand')
				r.append(sd_r_co.assign(NUM_CO_DAY = col.iloc[:,0], NB_CO_DAY= col.iloc[:,1]))
		self.df = pd.concat(r)
		print(datetime.datetime.now())
		print(self.df[['NUM_CO_DAY', 'NB_CO_DAY', "LAST_WIN_CO"]].describe())
		print(self.df[['NUM_CO_DAY', 'NB_CO_DAY', "LAST_WIN_CO"]])

		self.df.to_csv('./data/plat_enr.csv', index=False)
		
		
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