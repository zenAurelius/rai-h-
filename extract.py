
import pandas as pd
import numpy as np



class HraiExtractor:


	def run(self):
		self.df = pd.read_csv('./data/plat_enr1.csv', na_values = [''])
		
		self.df_2016 = self.df[(self.df.DATE_COURSE >= '2016-01-01') & (self.df.DATE_COURSE <= '2016-12-31') & (self.df.CONDUCTEUR.notna())].sort_values("REFERENCE", ascending=True)
		print(self.df_2016.describe())
		
		self.df_2016_16 = self.df_2016[(self.df_2016.NB_PARTANT == 16)]
		print(self.df_2016_16.describe())
		
		self.df_2016_16.to_csv('./data/plat_2016_16.csv', index=False)
		
ext = HraiExtractor()
ext.run()