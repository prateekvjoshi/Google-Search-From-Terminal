# coding: utf-8

#!/usr/bin/env python

import sys

from optparse import OptionParser
parser = OptionParser(
	version="0.1",   
	description = "Print google search results on the terminal.",
	usage = "%prog [-vr] [--view] [--results][--help] [--version]")
parser.add_option("-r","--results",action="store",type = "int",dest="results",help="display specified number of results, default is 10." )
parser.add_option("-v","--view",action="store",type = "int",dest="view",help="view page by index number." )    
(options,args) = parser.parse_args()
        		    
print "\nLoading...\n"
option = ""

for arg in args: option += arg+"+"

if len(option) == 0: parser.error("Please enter a search term")

from urllib import FancyURLopener

class MyOpener(FancyURLopener): version = '' # Google doesn't like the user agent, so send blank 


try:   
	s = MyOpener().open('http://www.google.com/search?q=%s'% option).read()
except IOError:
	print 'Could not connect to google, check your internet connection'

import re
dict = {}
entry = re.split('<li class=g><h3 class=r>',s) #split page by results
entry = entry[1:]                              #get rid of first bit
counter = 1
num_results = 5


i = 0

while i < num_results:
	i = i+1
	s = s.replace('\'',"'")                 
	s = s.replace('&amp;',"&")
	s = s.replace('&middot;',"\302\267")
	s = s.replace('&quot;','"')
	s = s.replace('&lt;','<')
	s = s.replace('&gt;','>')
	s = s.replace('本','\346\234\254')
	s = s.replace('日','\346\227\245')
	s = s.replace('&nbsp;',' ')
	s = s.replace('&#39;','\'')
	s = s.replace('Cached','\n')
    	
	entry = re.split('<br>',s)  # gets rid of last bits, cached and similar pages  etc
	s=entry[0]
    	
	a = s.find("<a href")     #get web address
	b = s.find("</a>")
	address = s[a:b]
	title = s[a:b]            # get title
	a = address.find('"')
	address = address[a+1:]
	b = address.find('"')
	address = address[:b]
    
	b = s.find("</a>")
	s = s[b:]                  
    
	s = re.sub('<.*?>','',s)
	title = re.sub('<.*?>','',title)    	                        
    	
    	
        s = s.replace('www','\nwww')
        s = s.replace('http','\nhttp')
    	
	print "\033[34;04m[%d] %s\033[00;00m" % (counter , title)
	print s[s.find("Show search tools")+17:]
	print "\033[32;01m%s\033[00;00m" % address
	print "-----------------------------------------------------------"
	dict[counter] = address
	if options.results == counter: break
	counter += 1
