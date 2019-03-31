#!/usr/bin/python3

import math

import pandas as pd
import numpy as np
import tensorflow as tf

from matplotlib import pyplot as plt
from matplotlib import cm

from sklearn import metrics

import operator

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

		tf.logging.set_verbosity(tf.logging.ERROR)
		pd.options.display.max_rows = 10
		pd.options.display.float_format = '{:.2f}'.format
		
	###############################################################################################
	# INIT MODELE
	def initModele(self, model) :
		

		columns = self.constructColumn()

		#optimizer = tf.train.ProximalAdagradOptimizer(learning_rate=0.1,l1_regularization_strength=0.001)
		optimizer = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate)
		optimizer = tf.contrib.estimator.clip_gradients_by_norm(optimizer, 5.0)
		'''
		self.model = tf.estimator.LinearRegressor(
    		feature_columns=columns,
    		optimizer=optimizer
		)
		'''
		#'''
		self.model = tf.estimator.DNNRegressor(
			model_dir=self.modelDir,
    		feature_columns=columns,
    		hidden_units=[40, 20, 20],
    		optimizer=optimizer)
		#'''
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
		columns.add(dist_buc)
		columns.add(tf.feature_column.indicator_column(sx_column))
		return columns

	###############################################################################################
	# LOAD FILE
	def loadFile(self, filename, balancing=False) :

		self.dataset = pd.read_csv(filename)

		if(balancing) :
			counts = self.dataset["TARGET"].value_counts()
			print(counts)
			df_loss = self.dataset[self.dataset["TARGET"] == 0]
			df_win = self.dataset[self.dataset["TARGET"] != 0]
			df_loss = df_loss.sample(counts.iloc[2])
			self.dataset = pd.concat([df_loss, df_win], axis=0)
			counts = self.dataset["TARGET"].value_counts()
			print(counts)

		print(self.dataset.head(10))
		self.dataset = self.dataset.reindex(np.random.permutation(self.dataset.index)).reset_index(drop=True)
		print(self.dataset.head(10))

		self.features = self.dataset.drop(columns=['TX_HIT_CO', 'LIEUX', 'PRIX', 'OEILLERE','RPT_COUPLE', 'RPT_TRIO', 'RPT_TIERCEO', 'RPT_TIERCED', 'RPT_QUARTEO', 'RPT_QUARTED', 'RPT_QUINTEO', 'RPT_QUINTED', 'TARGET', 'REFERENCE'])
		print("Features loaded :")
		print(self.features.head(10))
		print(self.features.describe())

		if "TARGET" in self.dataset.columns :
			#self.targets = self.dataset[["TARGET", "COTE"]].apply(lambda x : x.TARGET + x.COTE * x.TARGET, axis=1)
			self.targets = self.dataset["TARGET"]
			print("Targets loaded :")
			print(self.dataset[["TARGET", "COTE"]])
										
	###################################################################################################
	def train_input_fn(self, features, targets, batch_size=1, shuffle=True, num_epochs=None):
		
		features = {key:np.array(value) for key,value in dict(features).items()} 

		ds = tf.data.Dataset.from_tensor_slices((features,targets)) 
		ds = ds.batch(batch_size).repeat(num_epochs)
		if shuffle :
			ds = ds.shuffle(buffer_size=10000)

		features, labels = ds.make_one_shot_iterator().get_next()
		return features, labels
		
	###################################################################################################
	def eval_input_fn(self, features, labels=None, batch_size=None):
		
		if labels is None:
			inputs = features
		else:
			inputs = (features, labels)

		dataset = tf.data.Dataset.from_tensor_slices(inputs)
		assert batch_size is not None, "batch_size must not be None"
		dataset = dataset.batch(batch_size)
		return dataset.make_one_shot_iterator().get_next()

	###################################################################################################
	# TRAIN FROM FILE
	def trainFromFile(self, filename, filetosave, plotting=False, modelname = None):
		
		self.loadFile(filename, True)
		self.initModele(modelname)
		
		steps_per_period = self.steps / self.periods
		print(steps_per_period)
		self.preparePlot()

		print("training...")
		for period in range(0, self.periods) :
			self.model.train(
				input_fn = lambda:self.train_input_fn(self.features, self.targets, self.batch_size),
				steps = steps_per_period
			)
			self.eval(period)
		print("done.")

		self.dataset["PREDICTION"] = pd.Series(self.predictions)
		self.dataset.to_csv(filetosave)

		if plotting :
			self.drawPlot()
		

	###################################################################################################
	def drawPlot(self) :
		
		self.colors = [cm.coolwarm(x) for x in np.linspace(-1, 1, len(self.forPlot['linears']))]
		
		plt.figure(figsize=(15, 6))
		plt.subplot(1, 2, 1)
		plt.title("Learned Line by Period")
		plt.ylabel("RESULTAT")
		plt.xlabel("NUM_PARTICIPATION")
		sample = self.dataset.sample(n=300)
		
		x_0 = sample["NUM_PARTICIPATION"].min()
		x_1 = sample["NUM_PARTICIPATION"].max()

		for i, (w, b) in enumerate(self.forPlot['linears']) :
			y_0 = w * x_0 + b 
			y_1 = w * x_1 + b
			plt.plot([x_0, x_1], [y_0, y_1], color=self.colors[i])

		plt.scatter(sample["NUM_PARTICIPATION"], sample["TARGET"])

		plt.subplot(1, 2, 2)
		plt.title("RMSE")
		plt.plot(self.forPlot['RMSEs'])

		plt.show()

	
	###################################################################################################
	def preparePlot(self) :

		self.forPlot = {}
		self.forPlot['RMSEs'] = []
		self.forPlot['linears'] = []

	###################################################################################################
	def eval(self, period=0):
		
		predictions = self.model.predict(
			input_fn = lambda:self.train_input_fn(self.features, self.targets, num_epochs=1, shuffle=False)
		)

		pred_list = [item['predictions'][0] for item in predictions]
		#print(pred_list)
		self.predictions = np.array(pred_list)
		root_mean_squared_error = math.sqrt(metrics.mean_squared_error(self.predictions, self.targets))

		print("  periode %02d : %0.2f" % (period, root_mean_squared_error))
		#self.forPlot['RMSEs'].append(root_mean_squared_error)

		#weight = self.model.get_variable_value('linear/linear_model/NUM_PARTICIPATION/weights')[0]
		#bias = self.model.get_variable_value('linear/linear_model/bias_weights')

		#self.forPlot['linears'].append((weight, bias))
		
	###################################################################################################
	# EVAL FROM FILE
	def evalFromFile(self, filename, filetosave, plotting=False) :
		if self.model is None :
			print("Le modèle n'a pas été entrainé...")
			return
		
		self.loadFile(filename)

		self.preparePlot()

		self.eval()

		self.dataset["PREDICTION"] = pd.Series(self.predictions)
		self.dataset.to_csv(filetosave)

		if plotting :
			self.drawPlot()
		
	###################################################################################################
	# PREDICT FROM FILE
	def predictFromFile(self, filename, filetosave) :
	
		pass
		'''
		if self.model is None :
			print("Le modèle n'a pas été entrainé...")
			return
		
		self.loadFile(filename)		
		pred_dict = self.model.predict( input_fn=lambda:self.eval_input_fn(self.features, batch_size=512) )
		liste_pred = list(pred_dict)
		proba = [p['predictions'].tolist()[0] for p in liste_pred]
		self.features["eval"] = proba
		print(proba)
		print(self.labels)

	
		with open(filetosave, 'w', -1, 'utf-8') as f:
			json.dump({'features' : self.features, 'm' : self.numM, 'courses' : self.courses}, f, ensure_ascii=False)
		'''	

#**************************************************************************************************
ev = HraiEvaluator()
ev.trainFromFile('./data/train.hrd', './data/train.prd', plotting=False)
ev.evalFromFile('./data/train.hrd', './data/train.prd')
ev.evalFromFile('./data/dev.hrd', './data/dev.prd')

