
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
		pastOfCo = group[group.REFERENCE < row.REFERENCE].sort_values('REFERENCE', ascending=False).head(100)
		winOfCo = pastOfCo[pastOfCo['RESULTAT'] == 1]
		lastWin = np.flatnonzero(pastOfCo['RESULTAT'] == 1)
		last_win_co = 100
		if(len(lastWin) > 0) :
			last_win_co = lastWin[0] + 1
			
		tx_hit_co = 0
		if(len(pastOfCo) > 0) :
			tx_hit_co = len(winOfCo) / len(pastOfCo)
			
		return [last_win_co, tx_hit_co]
		
	def enr_ch_0(self, group, row) :
		print(self.nbT, end='\r')
		self.nbT += 1
		pastOfCh = group[group.REFERENCE < row.REFERENCE].sort_values('REFERENCE', ascending=False).head(100)
		winOfCh = pastOfCh[pastOfCh['RESULTAT'] == 1]
		plaOfCh = pastOfCh[(pastOfCh['RESULTAT'] == 2) | (pastOfCh['RESULTAT'] == 3)]
		lastWin = np.flatnonzero(pastOfCh['RESULTAT'] == 1)
		last_win_ch = 0
		if(len(lastWin) > 0) :
			last_win_ch = lastWin[0] + 1
			
		day_last_ch = 0
		if(len(pastOfCh) > 0) :
			date_r = datetime.datetime.strptime(pastOfCh.iloc[0].DATE_COURSE, "%Y-%m-%d")
			date_c = datetime.datetime.strptime(row.DATE_COURSE, "%Y-%m-%d")
			day_last_ch = (date_c - date_r).days
			
		tx_win_ch = 0
		tx_pla_ch = 0
		nb_past_ch = len(pastOfCh)
		if (nb_past_ch > 3) :
			tx_win_ch = len(winOfCh) / len(pastOfCh)
			tx_pla_ch = len(plaOfCh) / len(pastOfCh)
			
		return [last_win_ch, tx_win_ch, tx_pla_ch, nb_past_ch, day_last_ch]
		
	def enr_ch_1(self, group, row) :
		print(self.nbT, end='\r')
		self.nbT += 1
		pastOfCh = group[group.REFERENCE < row.REFERENCE].sort_values('REFERENCE', ascending=False).head(100)
		
		dcou_ch = 0
		if(len(pastOfCh) > 0) :
			date_r = datetime.datetime.strptime(pastOfCh.tail(1).iloc[0].DATE_COURSE, "%Y-%m-%d")
			date_c = datetime.datetime.strptime(row.DATE_COURSE, "%Y-%m-%d")
			nb_day_past = (date_c - date_r).days
			if (nb_day_past > 0) :
				dcou_ch = len(pastOfCh) / nb_day_past
					
		dpoids_last_ch = 0
		if(len(pastOfCh) > 0) :
			last_poids = pastOfCh.iloc[0].POIDS
			if(row.POIDS > 20 and last_poids > 20) :
				dpoids_last_ch  = (row.POIDS - last_poids) / row.POIDS
			
		return [dpoids_last_ch, dcou_ch]
			

	def run(self):
		#full = pd.read_csv('./data/full.csv')
		#self.df = full[full.TYPE_COURSE == 'p']
		#self.df.to_csv('./data/plat.csv', index=False)
		
		self.df = pd.read_csv('./data/plat_enr.csv')
		print(len(self.df))
		
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
		'''
		print(datetime.datetime.now())
		r = []
		dfs = []
		coco = self.df.groupby('CONDUCTEUR')
		self.nbT = 0
		for i, (u, r_co) in enumerate(coco) :
			# 1
			col = r_co.apply(lambda x : self.enr_co_0(r_co, x), axis=1, result_type='expand')
			r.append(r_co.assign(LAST_WIN_CO = col.iloc[:,0], TX_HIT_CO = col.iloc[:,1]))
			if(i%1000 == 0):
				dfs.append(pd.concat(r))
				r = []
		
		self.df = pd.concat(dfs)
		'''
		# 1 
		'''
		print(datetime.datetime.now())
		r = []
		dfs = []
		coco = self.df.groupby('CONDUCTEUR')
		print(len(coco))
		self.nbT = 0
		for i, (u, r_co) in enumerate(coco) :	
			sd_g_co = r_co.groupby('DATE_COURSE')
			for j, (_, sd_r_co) in enumerate(sd_g_co) :
				col = sd_r_co.apply(lambda x : self.enr_co_1(sd_r_co, x), axis=1, result_type='expand')
				r.append(sd_r_co.assign(NUM_CO_DAY = col.iloc[:,0], NB_CO_DAY= col.iloc[:,1]))
			if(i%100 == 0):
				dfs.append(pd.concat(r))
				r = []
				print(i)
				print(len(dfs))
		'''			
		print(datetime.datetime.now())
		self.nbT = 0
		r = []
		dfs = []
		g_ch = self.df.groupby('NOM_CHEVAL')
		print(len(g_ch))
		print(datetime.datetime.now())
		for i, (u, r_ch) in enumerate(g_ch) :
			# 1
			col = r_ch.apply(lambda x : self.enr_ch_1(r_ch, x), axis=1, result_type='expand')
			r.append(r_ch.assign(DPOIDS_LAST_CH = col.iloc[:,0], DCOU_CH = col.iloc[:,1]))
			if(i%2000 == 0):
				dfs.append(pd.concat(r))
				r = []
				
		self.df = pd.concat(dfs)
		print(datetime.datetime.now())
				
		self.df.to_csv('./data/plat_enr1.csv', index=False)
		
		
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