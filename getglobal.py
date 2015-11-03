import socket
import os
from bs4 import BeautifulSoup
import json
import urllib2


def getGlobalIp():
	url="http://globalipcheck.com/json/"
	page=urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	x = []
	x = json.loads(str(soup))
	return x['ip']



def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.bing.com', 0))
    return s.getsockname()[0]


print "Global IP address : " + getGlobalIp()
print "Local IP address : " + getNetworkIp()

