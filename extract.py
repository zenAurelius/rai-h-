
import pandas as pd
import numpy as np



class HraiExtractor:


	def run(self):
		self.lieux = ['DEAUVILLE','CHANTILLY','SAINT CLOUD','MAISONS LAFFITTE','LONGCHAMP','CAGNES SUR MER','MARSEILLE VIVAUX','COMPIEGNE','VICHY','TOULOUSE','LYON PARILLY','CLAIREFONTAINE','FONTAINEBLEAU','LA TESTE DE BUCH','LYON LA SOIE','MARSEILLE BORELY','PAU','PORNICHET LA BAULE','MONS','BORDEAUX LE BOUSCAT','LE CROISE LAROCHE','NANTES','KRANJI','NANCY','STRASBOURG','LE LION D ANGERS','ANGERS','AVENCHES','DEAUVILLE MIDI','AMIENS','SALON DE PROVENCE','MONT DE MARSAN','DAX','CHATEAUBRIANT','DIEPPE','ARGENTAN','CRAON','MOULINS','SAINT MALO','LE MANS','LES SABLES D''OLONNE','AIX LES BAINS','TARBES','LION D''ANGERS','CHOLET','LES SABLES','VITTEL','EVREUX','SENONNES','CARRERE','NIMES','CAVAILLON','AGEN','LIGNIERES','LE TOUQUET','ANGOULEME','MORLAIX','MACHECOUL','CARPENTRAS','VICHY SOIR','POMPADOUR','ROYAN LA PALMYRE','LA ROCHE POSAY','AUTEUIL','CHAMP DE MARS','NORT SUR ERDRE','SAINT MORITZ','PAU MIDI','HYERES','TOURS','AJACCIO','AVENCHES SOIR','MONTLUCON NERIS','CHAMPS DE MARS','DIVONNE LES BAINS','SABLE SUR SARTHE','CAGNES MIDI','BLAIN']

		self.df = pd.read_csv('./data/plat_enr2.csv', na_values = [''])
		self.df = self.df.loc[:, ~self.df.columns.str.contains('^Unnamed')]
		
		self.df = self.df[self.df['LIEUX'].isin(self.lieux)]
		self.df_2016 = self.df[(self.df.DATE_COURSE >= '2016-01-01') & (self.df.DATE_COURSE <= '2016-12-31') & (self.df.CONDUCTEUR.notna())].sort_values("REFERENCE", ascending=True)
		print(self.df_2016.describe())
		
		self.df_2016_16 = self.df_2016[(self.df_2016.NB_PARTANT == 16)]
		print(self.df_2016_16.describe())
		
		self.df_2016_16.to_csv('./data/plat_2016_16.csv', index=False)
		
ext = HraiExtractor()
ext.run()