#Libreries
from ast import And
import os
#Math
import numpy as np
#Dataframe
import pandas as pd
from pathlib import Path 

cwd = Path.cwd()
file_I = Path('In/diabetes.csv')
data_I = pd.read_csv(cwd / file_I)

columns = data_I.columns.tolist()

data_I.loc[:,'BMI']==0

data_I.loc[(data_I.loc[:,'BMI']==0) | (data_I.loc[:,'SkinThickness']==0) | (data_I.loc[:,'BloodPressure']==0)  ,:]


