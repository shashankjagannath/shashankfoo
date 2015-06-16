#! /bin/python
import time
import glob
import os
import subprocess
import types


subprocess.call("cat /var/tmp/rancid/router.db | grep juniper | grep -v fx | cut -d';' -f1 | grep -v fx | xargs -L1 -P30 sh -c '/usr/libexec/rancid/jlogin  -c \"show rsvp interface\" $0 > $0.rsvp'", shell=True)
subprocess.call("cat /var/tmp/rancid/router.db | grep juniper | grep -v fx | cut -d';' -f1 | grep -v fx | xargs -L1 -P30 sh -c '/usr/libexec/rancid/jlogin -c \"show isis adjacency\" $0 > $0.isis'", shell=True)
subprocess.call("cat /var/tmp/rancid/router.db | grep juniper | grep -v fx | cut -d';' -f1 | grep -v fx | xargs -L1 -P30 sh -c '/usr/libexec/rancid/jlogin  -c \"show isis interface brief\" $0 > $0.isis.costmap'", shell=True)

timestr = time.strftime("%Y%m%d-%H%M")

def read_rsvp ():
	sdict ={}
	for file in glob.glob("*.rsvp"):
		sdict[file] = (open(file).read().splitlines())
		os.remove(file)
	return sdict

def read_isis ():
	sdict ={}
	for file in glob.glob("*.isis"):
		sdict[file] = (open(file).read().splitlines())
		os.remove(file)
	return sdict

def read_isiscost ():
	sdict ={}
	for file in glob.glob("*.isis.costmap"):
		sdict[file] = (open(file).read().splitlines())
		os.remove(file)
	return sdict

def rsvpdictout (rsvp):
	dictrsvp = {}
	for keyrsvp in rsvp:
		for lrsvp in rsvp[keyrsvp]:
			if 'Up' in lrsvp:
				krsvp = keyrsvp.split('.')
				lr = lrsvp.split()
				if 'Mbps' in lr[5]:
					dictrsvp[krsvp[0], lr[0]] = (lr[4],lr[5],'Bottleneck!!!')
				else:
					dictrsvp[krsvp[0], lr[0]] = (lr[4])
	return dictrsvp

def isisdictout (isis):
	dictisis = {}
	for keyisis in isis:
		for lisis in isis[keyisis]:
			if 'Up' in lisis:
				kisis = keyisis.split('.')
				li = lisis.split()
				dictisis[kisis[0], li[0]] =(li[1])
	return dictisis

def isisdictcostout (isiscost):
	dictisiscost = {}
	for keyisiscost in isiscost:
		for lisiscost in isiscost[keyisiscost]:
			if 'Point' in lisiscost:
				kisiscost = keyisiscost.split('.')
				lic = lisiscost.split()
				dictisiscost[kisiscost[0], lic[0]] =(lic[7].split('/')[1])
	return dictisiscost


rsvp = read_rsvp()
isis = read_isis()
isiscost = read_isiscost()
dictrsvp = rsvpdictout(rsvp)
dictisis = isisdictout(isis)
dictisiscost= isisdictcostout(isiscost)
filename = 'mapout'
filename += timestr
outputfile = open(filename,'w')
filename2 = 'bottleneckout'
filename2 += timestr
outputfile2 = open(filename2,'w')

for routerkeys in dictrsvp:
	if (routerkeys in dictrsvp and routerkeys in dictisis and routerkeys in dictisiscost and type(dictrsvp[routerkeys]) is not types.TupleType ):
		outputfile.write( routerkeys[0] + ' ' + routerkeys[1] + ' ' + dictrsvp[routerkeys] + ' ' + dictisiscost[routerkeys] + ' <> ' + dictisis[routerkeys] + '\n')
	elif (routerkeys in dictrsvp and routerkeys in dictisis and routerkeys in dictisiscost and type(dictrsvp[routerkeys]) is types.TupleType ):
		outputfile.write( routerkeys[0] + ' ' + routerkeys[1] + ' ' + dictrsvp[routerkeys] [0] + ' ' + dictrsvp[routerkeys] [2] + ' ' + dictisiscost[routerkeys] + ' <> ' + dictisis[routerkeys] + '\n')
                outputfile2.write( routerkeys[0] + ' ' + routerkeys[1] + ' ' + dictrsvp[routerkeys] [0] + ' ' + dictrsvp[routerkeys] [2] + ' ' + dictisiscost[routerkeys] + ' <> ' + dictisis[routerkeys] + '\n')

