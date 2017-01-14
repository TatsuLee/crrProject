#! /usr/bin/env python
import numpy as np
import scipy as sp
import pandas as pd
import mibian as mb
import matplotlib.pyplot as plt

def payoff ( S0, K, r, vola , T, M, opType, modelType):
        """
	This function is to calculate the option payoff at present
	using binomial option pricing model

	Inputs:
	------------------------
	S0: present stock price
	K: strike price
	r: risk-free interest rate
	u: up factor
	T: terminal time(years)
	M: time steps
	opType: 'call'/'put', default value is call
	modelType: if choose 'vola', u is changed with volatility

	temp paras:
	-----------------------
	d: down factor, set as 1/u
	q: R.N. probability
	dt: time increment
	df: discounted factor
	
	Outputs:
	-----------------------
	discounted payoff of option at t=0
	"""

	# para set up
        dt = T / M
	if modelType == 'vola':
		u = np.exp(vola * np.sqrt(dt)) # use volatility 
		df = np.exp(-r * dt) # Continuous compounding IR
	else:
		u = vola # do not use volatility
		df = 1/(1+r) ** dt # Compounding IR
        d = 1 / u # down factor
        q = (1/df - d) / (u - d) # r.n. probability

	# intialization for stock price
	S = np.zeros((M+1,M+1), dtype = np.float64)
	S[0, 0] = S0
	z = 0
	for j in range(1, M + 1, 1):
		z += 1
		for i in range(z + 1):
			S[i, j] = S[0, 0] * (u ** j) * (d ** (i * 2))
	
	# calculate payoff at each node
	payoff = np.zeros((M+1, M+1), dtype = np.float64)
	z = 0
	if opType == 'call':
		for j in range(0, M + 1, 1):
			for i in range(z+1):
				payoff[i, j] = max(S[i, j] - K, 0)
			z += 1
	if opType == 'put':
		for j in range(0, M + 1, 1):
			for i in range(z+1):
				payoff[i, j] = max(K - S[i, j] , 0)
			z += 1
        # valuation discounted payoff by R.N. meansure
	payoffStar = np.zeros((M+1, M+1), dtype = np.float64)
	payoffStar[:, M] = payoff[:, M]
	z = M + 1
	for j in range(M - 1, -1, -1):
		z -=1
		for i in range(z):
			payoffStar[i, j] = (q * payoffStar[i, j + 1] + (1 - q) * payoffStar[i+1, j+1]) * df
	return payoffStar[0, 0]


