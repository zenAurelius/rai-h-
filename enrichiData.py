
import pandas as pd
import numpy as np
import datetime

###############################################################################
class Enrichisseur:

	#----------------------------------------------------------------------------------------------
	def enr_p(self, c) :
		#corection reference
		'''ref = c.REFERENCE
		id_nc = c.REFERENCE.find('C') + 1
		if len(ref[id_nc:]) == 1 :
			ref = ref[:id_nc] + '0' + ref[id_nc:]
		return ref'''
		#season
		month = c.DATE_COURSE[5:7]
		season = 4
		if month in ['12', '01', '02'] :
			season = 0
		if month in ['03', '04', '05'] :
			season = 1
		if month in ['06', '07', '08'] :
			season = 2
		if month in ['09', '10', '11'] :
			season = 3
		print(month, season)
		return season

	#----------------------------------------------------------------------------------------------
	def enr_co_p(self, pa, gr) :
		past_cr = gr[gr.REFERENCE < pa.REFERENCE]
		same_day_cr = gr[gr.REFERENCE.str[:6] == pa.REFERENCE[:6]]
		num_id_inday = np.flatnonzero(same_day_cr['REFERENCE'] == pa.REFERENCE)
		nb_cr_inday = len(same_day_cr)
		known_cr = len(past_cr)
		#wins = np.flatnonzero(past_cr['RESULTAT'] == 1)
		#last_win_co = 100
		#tx_hit_co = 0
		#if(len(wins) > 0) :
		#	last_win_co = len(past_cr) - wins[-1]
		#if(len(past_cr)) :
		#	tx_hit_co = len(wins) / len(past_cr)
		
		num_cr_inday = 0
		if (nb_cr_inday) :
			num_cr_inday = num_id_inday[0] + 1
		
		to_return = pd.Series([known_cr, nb_cr_inday, num_cr_inday], index=['CO_KNOWN_CR', 'CO_NB_INDAY', 'CO_NUM_INDAY'])
		return to_return

	#----------------------------------------------------------------------------------------------
	def enr_co(self, gr) :
		self.nbT += 1
		print('-- GROUPE --', self.nbT, end='\r')
		#print(gr.REFERENCE)
		gr = gr.sort_values('REFERENCE', ascending=True)
		cols = gr.apply(lambda pa : self.enr_co_p(pa, gr), axis=1)#,result_type='expand')
		#print(cols)
		return cols
	
	
	#----------------------------------------------------------------------------------------------
	def enr_cr(self, gr) :
		self.nbT += 1
		print('-- GROUPE --', self.nbT, end='\r')
		nb_part = len(gr)
		datas = pd.DataFrame()
		datas['ID'] = gr.index
		datas['P_MAL'] = len(gr[gr.SEXE_CHEVAL == 'M']) / nb_part
		datas['P_FEM'] = len(gr[gr.SEXE_CHEVAL == 'F']) / nb_part
		datas['M_POIDS'] = gr.POIDS.mean()
		datas['S_POIDS'] = gr.POIDS.std()
		datas['M_AGE_CHEVAL'] = gr.AGE_CHEVAL.mean()
		datas['S_AGE_CHEVAL'] = gr.AGE_CHEVAL.std()
		
		datas.set_index('ID', inplace=True)
		
		return datas

	#----------------------------------------------------------------------------------------------			
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

	#----------------------------------------------------------------------------------------------	
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
			
	#----------------------------------------------------------------------------------------------
	def run(self):
		#full = pd.read_csv('./data/full.csv')
		#self.df = full[full.TYPE_COURSE == 'p']
		#self.df.to_csv('./data/plat.csv', index=False)
		
		self.df = pd.read_csv('./data/plat.csv', index_col='ID')
		#self.df = self.df.tail(1000)
		print(len(self.df))
		print(self.df.describe())
		print(self.df.tail())
		
		print(datetime.datetime.now())
		
		# BY CO --
		'''
		self.nbT = 0
		by_co = self.df.groupby('CONDUCTEUR')
		print(len(by_co))
		new_data = by_co.apply(lambda gr : self.enr_co(gr)).reset_index(level=0).drop(columns=['CONDUCTEUR'])
		print(new_data)
		self.df = pd.concat([self.df, new_data], axis=1)
		'''

		# BY CR --
		self.nbT = 0
		by_cr = self.df.groupby('REFERENCE')
		print('nb groupe = ', len(by_cr))
		new_data = by_cr.apply(lambda gr : self.enr_cr(gr)).reset_index(level=0)
		print(new_data)
		self.df = pd.concat([self.df, new_data], axis=1)

		# FULL --
		'''self.df['SEASON'] = self.df.apply(lambda p : self.enr_p(p), axis=1)
		print(datetime.datetime.now())
		print(self.df)'''

		print(datetime.datetime.now())	
		self.df.to_csv('./data/plat_enr2.csv')
		

###############################################################################		
enr = Enrichisseur()
enr.run()