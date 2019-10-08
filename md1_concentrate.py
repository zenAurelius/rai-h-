#!/usr/bin/python3


import pandas as pd
import re
import numpy as np
import operator
from datetime import timedelta
import math

class md1_Concentrator:
	
	###############################################################################################
	# INIT
	###############################################################################################
	def __init__(self) :
		self.stats = None
		pd.options.display.max_rows = 16
		
	###############################################################################################
	#
	###############################################################################################
	def loadData(self, filename) :
		
		self.data = pd.read_csv(filename)
		
	###############################################################################################
	#
	###############################################################################################
	def concentrate(self, filename, filetosave, filetorerun) :
		self.loadData(filename)
		
		self.iniStats("num_part")
		self.iniStats("cote")

		courses = self.data.groupby('REFERENCE')
		for ref, course in courses:
			#print(ref)
			#print(course[["REFERENCE", "NUM_PARTICIPATION", "COTE"]])
			if(len(course) != 16):
				print('Erreur nbpartant sur ' + ref)
				continue
			if(course["RESULTAT_COURSE"].iloc[0] == 'Annulée') :
				print('Erreur annulation sur ' + ref)
				continue

			reel_result = list(map(int, course["RESULTAT_COURSE"].iloc[0].split('-')))
			#print(reel_result)
			rapports = course.iloc[0][['COTE', 'RPT_COUPLE', 'RPT_TRIO', 'RPT_TIERCEO', 'RPT_TIERCED', 'RPT_QUARTEO', 'RPT_QUARTED', 'RPT_QUINTEO', 'RPT_QUINTED']].tolist()
			#print(rapports)
			course = course.sort_values("NUM_PARTICIPATION", ascending=True)
			#print(course[['COTE', "RPT_COUPLE","RPT_TRIO","RPT_TIERCEO","RPT_TIERCED","RPT_QUARTEO","RPT_QUARTED","RPT_QUINTEO","RPT_QUINTED"]])
			#print(course[["REFERENCE", "NUM_PARTICIPATION", "COTE"]])

			#print(reel_result[0]-1)
			rapports[0] = course["COTE"].iloc[reel_result[0]-1]
			#print(rapports)
			
			sum_pred = course["PREDICTION"].agg(np.sum)
			course["PRED_POND"] = course["PREDICTION"].apply(lambda x: 100 * x / sum_pred)
			#course["EXPECTED_VALUE"] = course[["PRED_POND", "COTE"]].apply(lambda x: x['PRED_POND'] * x['COTE'] - 100, axis=1)
			#course = course.sort_values("PRED_POND", ascending=False)
			course = course.sort_values("PRED_POND", ascending=False)
			#print(course.head())
			pred_result = course["NUM_PARTICIPATION"].iloc[0:5].tolist()
			
			#print(pred_result)
			self.majStats("num_part", reel_result, pred_result, rapports)
			
			course = course.sort_values("COTE", ascending=True)
			pred_result_cote = course["NUM_PARTICIPATION"].iloc[0:5].tolist()
			#print(pred_result_cote)
			self.majStats("cote", reel_result, pred_result_cote, rapports)
			
						
		self.printStats()
		
	def printStats(self):
	
		for name, stat in self.stats.items():
			print(name)
			print("win SG = " + str(stat['nbG']) + " / " + str(stat['nbC']) + " = " + "{:0.2f}".format(stat['nbG'] * 100 / stat['nbC']) + " | " + "{:0.2f}".format(stat['sumG'] - stat['nbC']) + " = " + "{:0.2f}".format((stat['sumG'] - stat['nbC']) * 100 / stat['nbC']))
			if stat['nbTotCO'] > 0 :
				print("win CG = " + str(stat['nbCG']) + " / " + str(stat['nbTotCO']) + " = " + "{:0.2f}".format(stat['nbCG'] * 100 / stat['nbTotCO']) + " | " + "{:0.2f}".format(stat['sumCG'] - stat['nbTotCO']) + " = " + "{:0.2f}".format((stat['sumCG'] - stat['nbTotCO']) * 100 / stat['nbTotCO']))
			if stat['nbTotTO'] > 0 :
				print("win TO = " + str(stat['nbTO']) + " / " + str(stat['nbTotTO']) + " = " + "{:0.2f}".format(stat['nbTO'] * 100 / stat['nbTotTO']) + " | " + "{:0.2f}".format(stat['sumTO'] - stat['nbTotTO']) + " = " + "{:0.2f}".format((stat['sumTO'] - stat['nbTotTO']) * 100 / stat['nbTotTO']))
			
		
	###############################################################################################
	def majStats(self, compteur, reel_result, pred_result, rapports):
			
		stats = self.stats[compteur]
		stats['nbC'] += 1
		if reel_result[0] == pred_result[0] : 
			stats['nbG'] += 1
			stats['sumG'] += float(rapports[0])

		if rapports[1] > 0. :
			stats['nbTotCO'] += 1
			if (pred_result[0] == reel_result[0] and pred_result[1] == reel_result[1]) or (pred_result[0] == reel_result[1] and pred_result[1] == reel_result[0]) :
				stats['nbCG'] += 1
				stats['sumCG'] += rapports[1]
		
		if rapports[2] > 0. :	
			stats['nbTotTO'] += 1
			if (   (reel_result[0] == pred_result[0] and reel_result[1] == pred_result[1] and reel_result[2] == pred_result[2]) 
				or (reel_result[0] == pred_result[0] and reel_result[1] == pred_result[2] and reel_result[2] == pred_result[1])
				or (reel_result[0] == pred_result[1] and reel_result[1] == pred_result[0] and reel_result[2] == pred_result[2])
				or (reel_result[0] == pred_result[1] and reel_result[1] == pred_result[2] and reel_result[2] == pred_result[0])
				or (reel_result[0] == pred_result[2] and reel_result[1] == pred_result[0] and reel_result[2] == pred_result[1])
				or (reel_result[0] == pred_result[2] and reel_result[1] == pred_result[1] and reel_result[2] == pred_result[0]) ) :
				stats['nbTO'] += 1
				stats['sumTO'] += rapports[2]
					
	###############################################################################################
	def iniStats(self, compteur):
		if self.stats is None:
			self.stats = {}

		self.stats[compteur] = {}
		self.stats[compteur]['nbC'] = self.stats[compteur]['nbG'] = self.stats[compteur]['sumG'] = 0
		self.stats[compteur]['nbTotCO'] = self.stats[compteur]['nbCG'] = self.stats[compteur]['sumCG'] = 0
		self.stats[compteur]['nbTotTO'] = self.stats[compteur]['nbTO'] = self.stats[compteur]['sumTO'] = 0
		
		return self.stats[compteur]
	

ct = md1_Concentrator()
ct.concentrate('./data/train.prd', './data/train.ctr', '')
ct.concentrate('./data/dev.prd', './data/dev.ctr', '')