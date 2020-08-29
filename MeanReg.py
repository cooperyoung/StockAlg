'''
This program (will) contain four functions which implemenet a quantitative
trading strategy that uses the idea of regression to the mean  
'''

import pandas as pd
import quandl
import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf


'''
This function takes in a company's ticker as a string (COMP), 
two lengths of time to use for the rolling mean (m1 and m2),
and a range of time (start_date and end_date). It returns the
amount of money that would be made (as a pecent) following
the basic mean-regression strategy.
''' 

def compute_profit(COMP, m1, m2, start_date, end_date):

	# First we initialize all of our variables
	data = yf.download(COMP, start=start_date, end=end_date)
	stocks = 0.0
	cash = 10000.0
	m1_array = []
	m2_array = []
	m1_array = data['Adj Close'].rolling(m1).mean()
	m2_array = data['Adj Close'].rolling(m2).mean()

	# Now we go through the arrays of rolling mean to buy and sell
	# when the values of m1 and m2 cross each other
	for i in range(m1+1, len(m1_array)):
		if (m1_array[i] <= m2_array[i] and m1_array[i-1] > m2_array[i-1]):
			stocks = cash / data['Adj Close'][i]
			cash = 0;
		if (m1_array[i] >= m2_array[i] and m1_array[i-1] < m2_array[i-1] and stocks != 0):
			cash = stocks * data['Adj Close'][i]
			stocks = 0;

	# If we have stocks left over, sell them. Then, compute the profit
	if (cash == 0):
		cash = stocks * data['Adj Close'][-1]
	profit = ((cash - 10000.0)/10000.0) * 100


	# Print results and graph the stock price and rolling means
	print 'cash = ', cash
	print 'stocks = ', stocks
	print 'profit = ', profit, '%' 

	m1_array.plot()
	m2_array.plot()
	data['Adj Close'].plot()
	plt.show()


# Heres a test run with the S&P 500
compute_profit("SPY", 5, 20, "2017-01-01", "2020-01-01")

