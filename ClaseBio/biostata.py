from ast import Lambda
import numpy as np
import pandas as pd
import math
import scipy.stats as ss

def is_categorical(array_like):
    """
    Test if the array is categorical.

    Parameters
    ----------
    array_like : pandas.arrays
        Input array to be tested
    """
    return array_like.dtype.name == 'category'

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
    data_sig = pd.DataFrame(data = {'Name': data_in.columns, 'statistic': np.zeros(data_in.shape[1]), 'p': np.zeros(data_in.shape[1])})

    #check of type of variabel per column check for categorical
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
    coltitle ='Totales'
    d = {'per': [(CQ.loc['Totales',coltitle]/CQ.loc['Totales','Totales'])*100.00]}
    valn = pd.DataFrame(d)
    valn = valn.applymap(lambda x: " ({:.2f})".format(x))
    CQ.loc['Totales',coltitle] = CQ.loc['Totales',coltitle].astype(str)
    strval = CQ.loc['Totales',coltitle] + valn
    CQ.loc['Totales',coltitle] = strval.iloc[0,0]

    for cols in colnames:
        if(is_categorical(data_in[cols])):
            ctableT = pd.crosstab(data_in[cols],data_in[colgrouped],margins=True)
            ctableT = ctableT.drop('All')
            if(ctableT.shape[0]>1):
                ctablen = pd.crosstab(data_in[cols],data_in[colgrouped], normalize='columns',margins=True)*100.00
                ctablen = ctablen.applymap(lambda x: " ({:.2f})".format(x))
                stat, pvalue, dof, expected = ss.chi2_contingency(ctableT.loc[:,valueslist])
                ctableT = ctableT.astype(str)
                ctableT = ctableT + ctablen
                ctableT.rename(columns={'All':'Totales'}, inplace = True)
                data_sig.loc[data_sig.Name==cols,'p'] = pvalue
                data_sig.loc[data_sig.Name==cols,'statistic'] = stat
                if((ctableT.index == 0).any()):
                    ctableT = ctableT.drop(0)
                    ctableT.rename({1:cols}, inplace = True) 
                if(pvalue < 0.001):
                    ctableT.loc[ctableT.index[0], 'p'] = '<0.001'
                elif(pvalue < 0.01):
                    ctableT.loc[ctableT.index[0], 'p'] = '<0.01'
                else:
                    ctableT.loc[ctableT.index[0], 'p'] = "{:.3f}".format(pvalue) 
                ctableT = ctableT.dropna()
            else:
                ctableT.rename(columns={'All':'Totales'}, inplace = True) 
                ctableT.rename(index={ ctableT.index[0]: cols }, inplace = True)
                data_sig.loc[data_sig.Name==cols,'p'] = math.nan
                data_sig.loc[data_sig.Name==cols,'statistic'] = math.nan
                for col in ctableT.columns:
                    ctableT[col].values[:] = 0
                ctableT.loc[ctableT.index[0], 'p'] = 'NaN'
        else:
            x=[]
            dataset_numeric = pd.concat([data_in[cols], data_in[colgrouped]], axis=1)
            for coltitle in valueslist:
                x.append(dataset_numeric.loc[dataset_numeric[colgrouped] == coltitle,cols])
            correlation, pvalue = ss.kruskal(*x)
            ctableT = dataset_numeric.groupby(colgrouped).mean().T
            ctableT.columns = ctableT.columns.tolist()
            ctableT['Totales'] = dataset_numeric[cols].mean()
            ctableT = ctableT.applymap(lambda x: "{:.2f}".format(x))
            ctabled = dataset_numeric.groupby(ColGrouped).std().T
            ctabled.columns = ctabled.columns.tolist()
            ctabled['Totales'] = dataset_numeric[cols].std()
            ctabled = ctabled.applymap(lambda x: " ({:.2f})".format(x))
            ctableT = ctableT + ctabled
            data_sig.loc[data_sig.Name==cols,'p'] = pvalue
            data_sig.loc[data_sig.Name==cols,'statistic'] = correlation
            if(pvalue < 0.001):
                ctableT.loc[ctableT.index[0], 'p'] = '<0.001'
            elif(pvalue < 0.01):
                ctableT.loc[ctableT.index[0], 'p'] = '<0.01'
            else:
                ctableT.loc[ctableT.index[0], 'p'] = "{:.3f}".format(pvalue)
        CQ  =  pd.concat([CQ, ctableT])
    CQ = CQ.replace(np.nan,'',regex = True)
