'''
This program will take in a universe of companies 
(the S&P 500 for instance) and a month (usually the 
coming month) and outputs a txt file in the form of:

Ticker Symbol      m1      m2

where (m1, m2) are the bestrunnng mean lengths from
the past year. 

Note: There is also a currently unused function that can 
be used to predict what the next best (m1, m2) will be
'''

import datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import requests
from bs4 import BeautifulSoup 


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

	return profit

'''
# This graphs the stock's price, running means, and prints the profit made.
# This should be commented out before using other functions that use 
# compute_profit() or else you'll print a bunch of graphs

	# Print results and graph the stock price and rolling means
	print('cash = {}'.format(cash))
	print('stocks = {}'.format(stocks))
	print('profit = {}%'.format(profit))

	m1_array.plot()
	m2_array.plot()
	data['Adj Close'].plot()
	plt.show()

# Test run takes ~1s
compute_profit("ABBV", 30, 55, "2019-08-28", "2020-08-28")
'''


'''
This function takes in a company's ticker as a string (COMP)
and a time interval (YYYY-MM-DD), and returns returns the optimal 
lengths of runnings means (m1 and m2) for that time interval 
and the profit they result in.
'''

def opt_means(COMP, start_date, end_date):
	best_m1 = 0
	best_m2 = 0
	best_profit = 0

	# We range through various mean lengths and keep track of the best one
	for m1 in range(5, 60, 5):
		for m2 in range(10, 90, 5):
			if (m2 > m1):
				profit = compute_profit(COMP, m1, m2, start_date, end_date)
				if ( profit > best_profit):
					best_m1 = m1
					best_m2 = m2
					best_profit = profit

	return best_m1 , best_m2

# Test run takes ~24s
# best_m1, best_m2 = opt_means("ABT", "2019-08-28", "2020-08-28")
# print('best short mean = {} \t best long mean = {}'.format(best_m1, best_m2))



'''
This function takes in a company an date (as YYYY, MM) and 
prints the best (m1 m2) during the 12 pervious year-long periods.

This function should be used to predict the next best (m1, m2)
'''

def proj_means(COMP, year, month):
	best_m1s = []
	best_m2s = []

	start_dates = []
	end_dates = []
	for m in range(month, 13, 1):
		start_date = "{}-{}-28".format(year-2, str(m).zfill(2))
		end_date = "{}-{}-28".format(year-1, str(m).zfill(2))
		start_dates.append(start_date)
		end_dates.append(end_date)

		next_m1, next_m2 = opt_means(COMP, start_date, end_date)
		best_m1s.append(next_m1)
		best_m2s.append(next_m2)

	for i in range(len(best_m1s)):
		print('{}  to  {} \t'.format(start_dates[i], end_dates[i])),
		print('{} \t {}'.format(best_m1s[i], best_m2s[i]))

# Test run takes ~120s
# proj_means("SPY", 2020, 1)



'''
First we scrape data from wiki to get a list of S&P500 ticker 
symbols. Then for each company we compute their optimal means 
based of the previous year and write them to a .txt file
'''

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
page = requests.get(url)
htmltext = BeautifulSoup(page.text, features="html5lib")
table = htmltext.find("table", {"id": "constituents"})

s_and_p500 = []

for row in table.findAll('tr')[1:]:
	hyperlinkedticker = row.findAll('td')[0]
	s_and_p500.append(hyperlinkedticker.findAll('a')[0].contents[0])



# Range through the S&P500 and write the best means from the previous 
# year to our output file (uses tqdm & time.sleep for progress bar)
f = open("2019-01_Means.txt", "a")
for i in range(400, len(s_and_p500), 1):
	m1, m2 = opt_means(s_and_p500[i], "2017-12-28", "2018-12-28")
	f.write("{} \t {} \t {} \n".format(s_and_p500[i], m1, m2))

# Currently it's set to print the best means for January, 2019
# based on data from the previous year (run time ~2.5h)

