#Libreries
from ast import Lambda
import os
#Math
import numpy as np
#Dataframe
import pandas as pd
from pathlib import Path 
#graphical libs
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
#mi funciones
from biostata import populationtest
from biostata import ortest

#lectura de archivos
cwd = Path.cwd()
file_I = Path('In/diabetes.csv')
data_I = pd.read_csv(cwd / file_I)
dirout = 'out/'
outpath = Path(cwd,dirout)
outpath.mkdir(parents=True, exist_ok=True)

#delete all patients with incomplete BMI, SkinThickness, BloodPressure
list_drop = (data_I.loc[(data_I.loc[:,'BMI']==0) | (data_I.loc[:,'SkinThickness']==0) | (data_I.loc[:,'BloodPressure']==0)  ,:]).index
data_I.drop(list_drop, inplace = True)

#pruebas estadisticas
stats_p = populationtest(data_I, 'Outcome', data_I['Outcome'].unique().tolist(), outpath, 'diabetesTHOSfiltered')
ortest(data_I, 'Outcome',np.r_[0:8],outpath, 'ORfiltered')

#pruebas de agrupacion y funciones en pandas
columns = data_I.columns.tolist()
#outcome index row index no longer unique
data_test = data_I.copy()
data_test.set_index([('Outcome'),('Pregnancies')], inplace = True) 
data_test.index.tolist()

#group by column
data_test = data_I.copy()
data_test.groupby(by=['Outcome']).mean()
data_test.groupby(by=['Outcome']).std()
data_test.groupby(by=['Outcome']).std() / data_test.groupby(by=['Outcome']).mean()

#group by column but only one column in result
data_test.groupby(by=['Outcome'])['Pregnancies'].mean()

#aggregation multiple calculos over all columns
data_test.groupby(by=['Outcome']).agg(['min','max', 'mean', 'std'])
data_test.groupby(by=['Outcome']).Pregnancies.agg(['min','max', 'mean', 'std'])
data_test.groupby(by=['Outcome'])['Pregnancies'].agg(['min','max', 'mean', 'std'])

#loop
newcolumns = columns.copy()
newcolumns.remove('Outcome')
for column in newcolumns:
    print(column)
    data_test.groupby(by=['Outcome'])[column].agg(['min','max', 'mean', 'std'])

#different agg
data_test.groupby(by=['Outcome']).agg({'Insulin':['mean', 'std'], 'BMI':'sum'})

#my own operations
data_test.groupby(by=['Outcome']).Age.agg(lambda x: sum(x)+2)
data_test.groupby(by=['Outcome']).Age.agg(lambda x: np.std(x)/np.mean(x))

#graphical test
sns.set_theme(style = "ticks")

f, ax = plt.subplots(figsize=(7,5))
sns.despine(f)

logscale = False

sns.histplot(
    data_I,
    x="Age",
    hue="Outcome",
    palette="light:m_r",
    edgecolor =".3",
    linewidth = .5,
    log_scale=logscale,
    multiple="layer",
    kde=True,
    stat="probability"
    )
ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
ax.set_xticks([20, 30, 40, 50, 60, 70, 80, 90, 100])
plt.show()
plt.close()