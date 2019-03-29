
import pandas as pd
import numpy as np
import datetime

df = pd.read_csv('./data/plat_2017_16.csv')
df.drop('NUM_CO_DAY', axis=1)
print(df.describe())

coco = df.groupby('CONDUCTEUR')
print(len(df))
print(len(coco))
nbT = 0
def id_flat(group, row) :
	global nbT
	print(nbT, end='\r')
	nbT += 1
	
	idx = np.flatnonzero(group['REFERENCE'] == row.REFERENCE)
	nb_co_day = len(group)
	num_co_day = 0
	if(len(idx) > 0) :
		num_co_day = idx[0] + 1
	return [num_co_day, nb_co_day]
	
def id_flat0(group, row) :
	pastOfCo = group[group.REFERENCE < row.REFERENCE]
	lastWin = np.flatnonzero(pastOfCo['RESULTAT'] == 1)
	print(pastOfCo)
	print(lastWin)
	return [0, 0]

print(datetime.datetime.now())
nb_sd_g_co = 0
nb_sd_r_co = 0
r = []
for i, (u, r_co) in enumerate(coco) :
	# 1
	col = r_co.apply(lambda x : id_flat0(r_co, x), axis=1, result_type='expand')
	# 2
	sd_g_co = r_co.groupby('DATE_COURSE')
	nb_sd_g_co += len(sd_g_co)
	for j, (_, sd_r_co) in enumerate(sd_g_co) :
		# print(sd_r_co)
		nb_sd_r_co += len(sd_r_co)
		
		# print(r)
		col = sd_r_co.apply(lambda x : id_flat(sd_r_co, x), axis=1, result_type='expand')
		# print("0 :")
		# print(col.iloc[:,0])
		# print("1 :")
		# print(col.iloc[:,1])
		r.append(sd_r_co.assign(NUM_CO_DAY = col.iloc[:,0], NB_CO_DAY= col.iloc[:,1]))
		# print(sd_r_co[['NUM_CO_DAY', 'NB_CO_DAY']])

print(datetime.datetime.now())
dfu = pd.concat(r)
print(datetime.datetime.now())
print(dfu[['NUM_CO_DAY', 'NB_CO_DAY']].describe())
print(dfu[['NUM_CO_DAY', 'NB_CO_DAY']])

'''
print(datetime.datetime.now())
courses = df.groupby('REFERENCE')
print(len(courses))
print(datetime.datetime.now())
col_names = ['NUM_PARTICIPATION', 'POIDS', 'CORDE', 'COTE']	
df_trans = pd.DataFrame()
for i, (u, rows) in enumerate(courses) :
	min = rows[col_names].min()
	max = rows[col_names].max()
	df_trans = df_trans.append((rows[col_names] - min) / (max - min))
print(datetime.datetime.now())
df[['NUM_O', 'POIDS_O', 'CORDE_O', 'COTE_O']] = df_trans
print(df[['NUM_O', 'POIDS_O', 'CORDE_O', 'COTE_O']])
print(datetime.datetime.now())
'''

''' # FER
print(df.FER.value_counts(dropna=False))
'''

'''# HANDICAP
print(df.HANDICAP.value_counts(dropna=False))
print(df.HANDICAP.describe())
'''

'''# AGE_CHEVAL
print(df.AGE_CHEVAL.value_counts(dropna=False))
print(df.AGE_CHEVAL.describe())
'''

'''# SEASON
print(df.DATE_COURSE.describe())
seasons = pd.Series(df.DATE_COURSE.str.split('-', expand=True)[1], dtype='int64', name='SEASON').mod(12).floordiv(3)
newdf = pd.concat([df.DATE_COURSE, seasons], axis=1)
print(seasons.value_counts())
print(newdf[(newdf.DATE_COURSE > '2017-01-01') & (newdf.DATE_COURSE < '2017-02-31')])
print(newdf[(newdf.DATE_COURSE > '2017-03-01') & (newdf.DATE_COURSE < '2017-05-31')])
print(newdf[(newdf.DATE_COURSE > '2017-06-01') & (newdf.DATE_COURSE < '2017-08-31')])
print(newdf[(newdf.DATE_COURSE > '2017-09-01') & (newdf.DATE_COURSE < '2017-11-31')])
print(newdf[(newdf.DATE_COURSE > '2017-12-01') & (newdf.DATE_COURSE < '2017-12-31')])
'''

'''# ORDERED
def ordered(row,courses, col_names):
	to_return = []
	for col_name in col_names :
		print(row[col_name])
		min, max = courses.get_group(row.REFERENCE)[col_name].agg(['min', 'max'])
		val = 0
		if(max - min > 0) :
			val = 2 * ((row[col_name] - min) / (max - min)) -1
		to_return.append(val)
	return to_return
	
courses = df.groupby('REFERENCE')

print(df.iloc[[0]])
df.iloc[[0]].apply(lambda x : ordered(x, courses, ['NUM_PARTICIPATION', 'POIDS', 'CORDE', 'COTE']), axis=1)
'''

# PERIODE
#print(df.HEURE.value_counts())


''' # OEILLERE
df_win = df[df.RESULTAT == 1]
print('full win = {0}'.format(100 * len(df_win) / len(df)))

print(df.OEILLERE.value_counts(dropna=False))
df_oeil = df[df.OEILLERE.notna()]
df_notoeil = df[df.OEILLERE.isna()]

df_oeil_win = df_oeil[df_oeil.RESULTAT == 1]
df_notoeil_win = df_notoeil[df_notoeil.RESULTAT == 1]
print('OEIL = {0} / {1} : {2}'.format(len(df_oeil), len(df_oeil_win), 100 * len(df_oeil_win) / len(df_oeil)))
print('NOTO = {0} / {1} : {2}'.format(len(df_notoeil), len(df_notoeil_win), 100 * len(df_notoeil_win) / len(df_notoeil)))

df['OEIL_T'] = df.OEILLERE.notna().astype(float)
print(df.OEIL_T.value_counts(dropna=False))
''' 
