'''
This program takes in a txt file of the form 

Ticker Symbol      m1      m2

where (m1, m2) are the best runnng mean lengths from
the past year and simulates a mean regression alg.

Every week it finds the ten stocks where m1 and m2 are 
closest, and buys/shorts them. We rebalance our 
portfolio every week, though this arbiraty length
could be optimized.
'''

import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date, timedelta
from heapq import nlargest, nsmallest


# Define a class to store our stock data (ticker symbol
# and optimal means for this month). Our sortkey indicates
# how close the running means currently are.
class Stock:
	def __init__(self, ticker, m1, m2):
		self.ticker = ticker
		self.m1 = m1
		self.m2 = m2

def sortkey(stock, current_date):
	early_date = current_date - timedelta(days = int(stock.m2))
	try:
		data = yf.download(stock.ticker, start = early_date, end = current_date)['Adj Close']
		difference = data.rolling(int(stock.m2)).mean()[-1] - data.rolling(int(stock.m1)).mean()[-1]
		return abs(difference)
	except:
		return float('inf')

def to_string(stock):
	return("Ticker: {} \t Means: ({}, {})".format(stock.ticker, stock.m1, stock.m2))

# returns information about a stock in the form
# [this weeks open price,  next weeks close price,  +-1]
# where +1 means buy and -1 means short
def info(stock, current_date):
	past_m2 = current_date - timedelta(days = 2*int(stock.m2))
	next_week = current_date + timedelta(days = 8)
	key_info = []
	data = yf.download(stock.ticker, start = past_m2, end = next_week)
	m1_array = data['Adj Close'].rolling(int(stock.m1)).mean()
	m2_array = data['Adj Close'].rolling(int(stock.m2)).mean()

	key_info .append(data['Open'][current_date.isoformat()])
	key_info .append(data['Close'][-1])
	if (m1_array[-3]) > m1_array[-1]:
		key_info.append(1)
	else:
		# CHANGE THIS BACK, I'M JUST TESTING SOMETHING
		key_info.append(-1)

	return key_info



# Read in our txt file into a list of Stock data types
direc = "/Users/cooperyoung/Desktop/Stocks/StockAlg/Optimal Means for 2019/2019-01_Means.txt"
f = open(direc, "r")
universe = []

for line in f:
	if (line.split()[1] != '0'):
		newstock = Stock(line.split()[0], line.split()[1], line.split()[2])
		universe.append(newstock)



# Set up our timeframe for the backtest 
start_date = date(2019, 1, 2)
end_date = date(2019, 1, 19)
test_days = end_date - start_date

cash = 10000.0

# Each week pick the 25 stocks with most potenetial 
# (meaning their rolling means are the cloest) 
# and buy/short. Print the money made
for i in range(0, test_days.days + 1, 7):
	this_week = start_date + timedelta(days=i)

	hot_stocks = []
	hot_stocks = nsmallest(25, universe, key = lambda stock: sortkey(stock, this_week))
	for stock in hot_stocks:
		print(to_string(stock))

	hot_info = []
	price_sum = 0.0
	for i in range(len(hot_stocks)):
		new_info = info(hot_stocks[i], this_week)
		hot_info.append(new_info)
		price_sum += new_info[0]


	new_cash = 0.0
	for i in range(len(hot_info)):
		new_cash += (hot_info[i][1]-hot_info[i][0])*hot_info[i][2]*cash/price_sum

	cash += new_cash

	for l in hot_info:
		print(l)

	print(cash)
	print("Percentage growth: {}%".format(((cash-10000.0)/10000)*100))

