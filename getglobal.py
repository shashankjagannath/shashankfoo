from bs4 import BeautifulSoup
import json
import urllib2

url="http://globalipcheck.com/json/"
page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
x = []
x = json.loads(str(soup))
print x['ip']
