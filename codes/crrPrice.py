#! /usr/bin/env python
import numpy as np
import scipy as sp
import pandas as pd
import mibian as mb
import matplotlib.pyplot as plt
import crrModel

"""
Part1: Reading option,stock Data From file
"""
# read data from csv data file
opData = pd.read_csv('geOpQuotes.txt')
stData = pd.read_csv('geStPrice.txt')
n = len(opData)  # number of options to price
unPrice = stData['adjClose'][0] # current underlying price of stock
r = 0.01 # risk-free insterest rate


"""
Part2: calculation of u(up factor in crr model)

Step1: select ATM option data
Step2: define function F(u)=crrModel.payoff(.,u)-optionPrice
Step3: use a non-linear solver to solve for u
"""
uData = opData[(opData['strike']==round(unPrice*2)/2)] # find data of ATM option
k = len(uData) # number of u's used for calibration
u = np.zeros(k, dtype=np.float64)
for i,j in zip(uData.index,range(k)):
	def F(u):
		return crrModel.payoff(unPrice,uData['strike'][i],r, u,\
			uData['deltaT'][i]/365.0, uData['deltaT'][i],\
			uData['opType'][i],'novola')-uData['ask'][i]
	
	u[j] = sp.optimize.newton_krylov(F, 1.02)

pd.DataFrame({'u':u, 'terDate':uData['terDate'], 'opType':uData['opType']}).to_csv('geUpFactor.txt')

"""
Part3: calculation of listed option price

opPriceU: use crr model without volatility
opPriceVola1: use crr model with calculated vola (used 'mibian.BS' model)
opPriceVola0: use crr model with given vola
"""
# create temp para 
opPriceVola0 = np.zeros( n , dtype = np.float64) # payoff using given implied volatility
opPriceVola1 = np.zeros( n , dtype = np.float64) # payoff using implied volatility 
opPriceU = np.zeros( (n,k) , dtype = np.float64) # payoff using u
imVola1 = np.zeros( n, dtype = np.float64) # implied volatility

# calculate implied volatility and option price for each contract
for i in range(n): 
		if opData['deltaT'][i] <= 0: continue # incase expired options are still on website
		if opData['opType'][i]=='call':
			c = mb.BS( [ unPrice, opData['strike'][i], r, opData['deltaT'][i] ],\
					callPrice = opData['ask'][i])
			imVola1[i] = c.impliedVolatility/100.0
		else:
			p = mb.BS( [ unPrice, opData['strike'][i], r, opData['deltaT'][i] ],\
					putPrice = opData['ask'][i])
			imVola1[i] = p.impliedVolatility/100.0
		
		opPriceVola1[i] = crrModel.payoff( unPrice, opData['strike'][i], r, imVola1[i],\
				opData['deltaT'][i]/365.0,  opData['deltaT'][i],\
				opData['opType'][i],'vola')
		opPriceVola0[i] = crrModel.payoff( unPrice, opData['strike'][i], r, opData['imVola0'][i],\
				opData['deltaT'][i]/365.0,  opData['deltaT'][i],\
				opData['opType'][i],'vola')
		
		for j in range(k):
			opPriceU[i,j] = crrModel.payoff( unPrice, opData['strike'][i], r,u[j] ,\
					opData['deltaT'][i]/365.0,  opData['deltaT'][i],\
					opData['opType'][i],'novola' )
print 'calculation of option price --- Done!'


# writing data to files
for i in range(k):
	opData['opPriceU%d'%i]=pd.Series(opPriceU[:,i],index=opData.index)
	opData['errPriceU%d'%i]=pd.Series(np.abs(opData['opPriceU%d'%i]-opData['ask'])/opData['ask'],\
			index=opData.index)
opData['imVola1']=pd.Series(imVola1,index=opData.index)
opData['errVola']=pd.Series(np.abs(opData['imVola1']-opData['imVola0'])/opData['imVola0'],\
		index=opData.index)
opData['opPriceVola1']=pd.Series(opPriceVola1,index=opData.index)
opData['errPriceVola1']=pd.Series(np.abs(opData['opPriceVola1']-opData['ask'])/opData['ask'],\
		index=opData.index)
opData['opPriceVola0']=pd.Series(opPriceVola0,index=opData.index)
opData['errPriceVola0']=pd.Series(np.abs(opData['opPriceVola0']-opData['ask'])/opData['ask'],\
		index=opData.index)

opData.to_csv('geOpPriceOut.txt')

