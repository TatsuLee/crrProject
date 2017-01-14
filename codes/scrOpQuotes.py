#! /usr/bin/env python
#coding=utf-8
"""
This program is to scrape GE options quotes 
from  fiance.yahoo website

Author: Da Li		Nov 2, 2014

"""
import os
import datetime as dt
import time
from calendar import datetime
import urllib2
from bs4 import BeautifulSoup as BS
ls=os.linesep

# creat a txt file  to store data
f=open('geOpQuotes.txt','w')
# write header for data
f.write('terDate'+','\
	+'deltaT'+','\
        +'opType'+',' \
	+'strike'+ ',' \
	+'contract'+',' \
	+'last'+',' \
	+'bid'+',' \
	+'ask'+',' \
	+'change'+',' \
	+'%change'+',' \
	+'volume'+',' \
	+'openInterest'+',' \
	+'imVola0'+ls)
# define url, search for datelist of option quotes
n= 0
url="http://finance.yahoo.com/q/op?s=GE"
terDate = BS(urllib2.urlopen(url)).find_all('option') # terminal date of op, listed  on website
today = dt.datetime.utcnow().replace(hour=0,minute=0,second=0,microsecond=0)
for t in terDate:
	# create soup obj
	timestamp = timegm(time.strptime(t.text+'GMT', '%B %d, %Y%Z')) # same as terDate
	url= "http://finance.yahoo.com/q/op?s=GE" + '&date=' + str(timestamp) 
	data=BS(urllib2.urlopen(url)).find_all('td') # this is  the op data
	i=3
	# write data into file
	while i<=len(data)-9:
		if data[i].text==u'\n\n\n\u2715\n[modify]\n\n':
			i +=1
		f.write( '20'+data[i+1].text[3:9]+',') # write terDate
		deltaT = dt.datetime.utcfromtimestamp(timestamp) - today
		f.write( str(deltaT.days) + ',' ) # write days to terminial date
		if data[i+1].text[9:10]=='C':
			f.write('call') # o stand for call
		else:
			f.write('put') # 1 stand for put

		for j in range(i, i+10, 1):
			if j == i+9:
				f.write(','+ str(float(data[j].text[1:-1].strip('%'))/100)  )
			else:
				f.write(','+ data[j].text[1:-1]) # write all other data
		i +=10
		f.write(ls)
	print( "scraping GE option on %s --- Done!"%  t.text) 
f.close()

