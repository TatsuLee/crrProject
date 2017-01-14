#! /usr/bin/env python
import numpy as np
import scipy as sp
import pandas as pd
import mibian as mb
import matplotlib.pyplot as plt
import crrModel


"""
 Calculate Option Price on March 15, 2015
"""
# find closest listed option to get strike price
opData=pd.read_csv('geOpQuotes.txt')
stData=pd.read_csv('geStPrice.txt')
uData=pd.read_csv('geUpFactor.txt')
opData=opData[(opData['terDate']==20150320)]
unPrice=stData['adjClose'][0]
ucOpt=uData['u'][2]
upOpt=uData['u'][1]
r=0.01
n=len(opData)
opPrice=np.zeros(n, dtype=np.float64)
opData.index=[a for a in range(n)]
for i in opData.index:
	if opData['opType'][i]=='call':
		opPrice[i]=crrModel.payoff(unPrice, opData['strike'][i],r,\
				ucOpt, (opData['deltaT'][i]-5)/365.0,\
				opData['deltaT'][i]-5,opData['opType'][i],'novola')
	else:
		opPrice[i]=crrModel.payoff(unPrice, opData['strike'][i], r,\
				upOpt, (opData['deltaT'][i]-5)/365.0,\
				opData['deltaT'][i]-5,opData['opType'][i],'novola')


opData['opPrice']=opPrice
opData=opData[['terDate','opType','strike','opPrice']]
opData.to_csv('ge20150315.txt',index=False)


