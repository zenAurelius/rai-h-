
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


###################################################################################################
class HraiEvaluator:

	###############################################################################################
	# INIT
	###############################################################################################
	def __init__(self, modeldir = None) :
		self.modelDir = modeldir
		self.model = None

		self.learning_rate = 0.01
		self.steps = 500
		self.batch_size = 5
		self.periods = 10
		self.features_names = ['NUM_0', 'POIDS_O', 'CORDE_O', 'COTE_O', 'LAST_WIN_CO','NB_CO_DAY','NUM_CO_DAY','HANDICAP','AGE_CHEVAL','SEXE_CHEVAL']

		tf.logging.set_verbosity(tf.logging.ERROR)
		pd.options.display.max_rows = 10
		pd.options.display.float_format = '{:.2f}'.format

	###############################################################################################
	# TRAIN FROM FILE
	###############################################################################################
	def trainFromFile(self, filename, filetosave, modelname = None):
		
		# charger / traiter les données
		self.loadFile(filename, True)
		# initialiser / compiler le modèle
		self.initModele(modelname)
		# entrainer le modèle
		features = self.dataset[self.features_names]
		targets = self.dataset["TARGET"]
		history = self.model.fit(
			features, targets,
			epochs=150)

		# enregistrer les prédictions
		'''self.dataset["PREDICTION"] = pd.Series(self.predictions)'''
		'''self.dataset.to_csv(filetosave)'''

		features = self.original_dataset[self.features_names]
		result =self.model.predict(features)
		self.original_dataset["PREDICTION"] = pd.Series(result.flatten())
		self.original_dataset.to_csv(filetosave)
	
	###############################################################################################
	# LOAD FILE
	###############################################################################################
	def loadFile(self, filename, balancing=False) :

		self.original_dataset = pd.read_csv(filename)
		print(self.original_dataset.describe())

		if(balancing) :
			print('balancing...')
			counts = self.original_dataset["TARGET"].value_counts()
			print('counts before :\n',counts)
			df_loss = self.original_dataset[self.original_dataset["TARGET"] == 0]
			df_win = self.original_dataset[self.original_dataset["TARGET"] != 0]
			df_loss = df_loss.sample(counts.iloc[2])
			self.dataset = pd.concat([df_loss, df_win], axis=0)
			counts = self.dataset["TARGET"].value_counts()
			print('counts after : \n',counts)
		else :
			self.dataset = self.original_dataset

		self.dataset = self.dataset.reindex(np.random.permutation(self.dataset.index)).reset_index(drop=True)
		

	###############################################################################################
	# INIT MODELE
	###############################################################################################
	def initModele(self, model) :
		

		#columns = self.constructColumn()

		self.model = keras.Sequential([
			layers.Dense(64, activation=tf.nn.relu, input_shape=[len(self.features_names)]),
			layers.Dense(128, activation=tf.nn.relu),
			layers.Dense(64, activation=tf.nn.relu),
			layers.Dense(1)
		])

		#optimizer = tf.keras.optimizers.RMSprop(0.001)
		optimizer = tf.keras.optimizers.Adam(lr=0.001)

		self.model.compile(	loss='mean_squared_error',
						optimizer=optimizer,
						metrics=['mean_absolute_error', 'mean_squared_error'])
		self.model.summary()
		
	###############################################################################################
	# CONSTRUCT COLUMN
	###############################################################################################
	def constructColumn(self):
 
		# ['LIEUX', 'DISTANCE', 'PRIX', 'SEXE_CHEVAL', 'SEASON', 'OEILLERE']
		dist_num = tf.feature_column.numeric_column("DISTANCE")
		dist_buc = tf.feature_column.bucketized_column(dist_num, boundaries=[1600, 2000, 2500])

		sx_column = tf.feature_column.categorical_column_with_vocabulary_list(
        	key="SEXE_CHEVAL",
        	vocabulary_list=["M", "H", "F"])
		
		# TODO : 'TX_HIT_CO'
		num_features = ['NUM_0', 'POIDS_O', 'CORDE_O', 'COTE_O', 'LAST_WIN_CO','NB_CO_DAY','NUM_CO_DAY','HANDICAP','AGE_CHEVAL' ]
		columns = set([tf.feature_column.numeric_column(feature_name) for feature_name in num_features])
		#columns.add(dist_buc)
		#columns.add(tf.feature_column.indicator_column(sx_column))

		return columns	

###################################################################################################

ev = HraiEvaluator()
ev.trainFromFile('./data/train.hrd', './data/train.prd')