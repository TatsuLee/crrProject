#! /usr/bin/env python
import numpy as np
import scipy as sp
import pandas as pd
import mibian as mb
import matplotlib.pyplot as plt
import os
ls=os.linesep

"""
Part1: Reading option,stock Data From file
"""
# read data from csv data file
opData=pd.read_csv('geOpPriceOut.txt')
stData = pd.read_csv('geStPrice.txt')
uData = pd.read_csv('geUpFactor.txt')
k = len(uData)  # number of u 
cData = opData[(opData['opType']=='call')]
pData = opData[(opData['opType']=='put')]
"""
Part2: Testing results--model:crr with u
"""
f=open('geUcallStats.txt', 'w')
f.write('u'+','+ 'errMean' +',' +'errStd'+ls)
for i in range(k):
	f.write(str(uData['u'][i])+','\
			+str(sp.mean(cData['errPriceU%d'%i]))+','\
			+str(sp.std(cData['errPriceU%d'%i]))+ls)
f.write('imVola1'+','\
		+str(sp.mean(cData['errPriceVola1']))+','\
		+str(sp.std(cData['errPriceVola1']))+ls)
f.write('imVola0'+','\
		+str(sp.mean(cData['errPriceVola0']))+','\
		+str(sp.std(cData['errPriceVola0']))+ls)
f.close()

f=open('geUputStats.txt', 'w')
f.write('u'+','+ 'errMean' +',' +'errStd'+ls)
for i in range(k):
	f.write(str(uData['u'][i])+','\
			+str(sp.mean(pData['errPriceU%d'%i]))+','\
			+str(sp.std(pData['errPriceU%d'%i]))+ls)
f.write('imVola1'+','\
		+str(sp.mean(pData['errPriceVola1']))+','\
		+str(sp.std(pData['errPriceVola1']))+ls)
f.write('imVola0'+','\
		+str(sp.mean(pData['errPriceVola0']))+','\
		+str(sp.std(pData['errPriceVola0']))+ls)
f.close()


"""
Part4: Plot
"""
ucOpt=2
upOpt=1
ucOptValue=uData['u'][ucOpt]
upOptValue=uData['u'][upOpt]
col=4
row=np.ceil(cData['terDate'].nunique()/float(col))

# call option plot, model: crr with u
for i,j in zip(cData['terDate'].unique(), range(cData['terDate'].nunique())):
	data = cData[(cData['terDate']==i)]
	plt.subplot(row, col , j+1)
	plt.title('%sC' %i)
	plt.xlabel('strike price')
	plt.ylabel('option price')
	plt.plot(data['strike'],data['opPriceU%d'%ucOpt], 'r+', label='pred price')
	plt.plot(data['strike'],data['ask'], 'go', label='market price')
	plt.legend(prop={'size':9})
plt.tight_layout(pad=0.1, w_pad =0.1, h_pad=0.1)
plt.show()

# put option plot, model: crr with u
for i,j in zip(pData['terDate'].unique(), range(pData['terDate'].nunique())):
	data = pData[(pData['terDate']==i)]
	plt.subplot(row, col , j+1)
	plt.title('%sP' % i)
	plt.xlabel('strike price')
	plt.ylabel('option price')
	plt.plot(data['strike'],data['opPriceU%d'%upOpt], 'r+', label='pred price')
	plt.plot(data['strike'],data['ask'], 'go', label='market price')
	plt.legend(loc=2, prop={'size':9})
plt.tight_layout(pad=0.8, w_pad =0.8, h_pad=1.0)
plt.show()


# call option plot, model: crr with imVola
for i,j in zip(cData['terDate'].unique(), range(cData['terDate'].nunique())):
	data = cData[(cData['terDate']==i)]
	plt.subplot(row, col , j+1)
	plt.title('%sC' %i)
	plt.xlabel('strike price')
	plt.ylabel('option price')
	plt.plot(data['strike'],data['opPriceVola1'], 'r+', label='pred price')
	plt.plot(data['strike'],data['ask'], 'go', label='market price')
	plt.legend(prop={'size':9})
plt.tight_layout(pad=0.1, w_pad =0.1, h_pad=0.1)
plt.show()

# put option plot, model: crr with imVola
for i,j in zip(pData['terDate'].unique(), range(pData['terDate'].nunique())):
	data = pData[(pData['terDate']==i)]
	plt.subplot(row, col , j+1)
	plt.title('%sP' % i)
	plt.xlabel('strike price')
	plt.ylabel('option price')
	plt.plot(data['strike'],data['opPriceVola1'], 'r+', label='pred price')
	plt.plot(data['strike'],data['ask'], 'go', label='market price')
	plt.legend(loc=2, prop={'size':9})
plt.tight_layout(pad=0.8, w_pad =0.8, h_pad=1.0)
plt.show()

