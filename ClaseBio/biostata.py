from ast import Lambda
import numpy as np
import pandas as pd
import math

data_in = data_I.copy()
colgrouped = 'Outcome'
valueslist = data_I['Outcome'].unique().tolist()
outpath = outpath
filename = 'diabetesTHOS'

def populationtest(data_in, colgrouped, valueslist, outpath, filename):
    """
    Test of indepence between populations. 

    Parameters
    __________
    data_in : Dataframe
        Input dataframe with the data to be tested
    colgrouped : pandas.column
        column
    collist : list of str
        list of columns to be tested
    """
    #list of significance
    data_sig = pd.DataFrame(data = {'Name': data_in.columns, 'statistic': np.zeros(data_in.shave[1]), 'p': np.zeros(data_in.shave[1])})

    #check of type of variabel per column
    data_in.loc[:, data_in.dtypes == 'object'] =\
        data_in.select_dtypes(['object']).apply(lambda x: x.astype('category'))
    data_in.loc[:, data_in.isin([0,1]).all()] = data_in.loc[:, data_in.isin([0,1]).all()].apply(lambda x: x.astype('category'))

    #columns test
    colnames = data_in.columns
    colnames = np.delete(colnames, [np.r_[colnames.get_loc(colgrouped)]], 0)

    valueslistconst = valueslist.copy()
    valueslistconst.extend(['Totales', 'p'])
    CQ = pd.DataFrame(columns = valueslistconst)
    temp_totales = data_in[colgrouped].value_counts()
    CQ.loc['Totales', 'Totales'] = 0
    for coltitle in valueslist:
        CQ.loc['Totales', coltitle] = temp_totales[coltitle]
        CQ.loc['Totales', 'Totales'] = CQ.loc['Totales', 'Totales'] + temp_totales[coltitle]
    for coltitle in valueslist:
        d={'per' : [(CQ.loc['Totales', coltitle]/CQ.loc['Totales', 'Totales'])*100.00]}
        valn = pd.DataFrame(d)
        valn = valn.applymap(lambda x: "({:.2f})".format(x))
        CQ.loc['Totales', coltitle] = CQ.loc['Totales', coltitle].astype(str)
        strval = CQ.loc['Totales', coltitle] + valn
        CQ.loc['Totales', coltitle] = strval.iloc[0,0]