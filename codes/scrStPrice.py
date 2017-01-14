#! /usr/bin/env python
#coding=utf-8
"""
This program is to scrape GE stock prices(past 3 months) 
from  fiance.yahoo website

Author: Da Li		Nov 2, 2014

"""
import os
import datetime as dt
import urllib2
from bs4 import BeautifulSoup as BS
ls=os.linesep

# creat a txt file  to store data
f=open('geStPrice.txt','w')
# write header for data
f.write('Date'+','\
	+'Open'+','\
        +'High'+',' \
	+'Low'+ ',' \
	+'Close'+',' \
	+'Volume'+',' \
	+'adjClose'+ls) 
# define url, search for stock price data
i = 0
url="http://finance.yahoo.com/q/hp?s=GE"
data = BS(urllib2.urlopen(url)).find_all('td',{'class':'yfnc_tabledata1'}) 

# write data into file
while i<=len(data)-6:
	if 'Dividend' in data[i+1].text:
		i +=2
	for j in range(i, i+7, 1):
		if j == i: f.write(data[j].text)
		else: f.write(','+ data[j].text) 
	i +=7
	f.write(ls)
print "scraping GE stock price --- Done!"  
f.close()
