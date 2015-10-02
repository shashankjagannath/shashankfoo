import time
import glob
import os
import types
import socket

def read_paths ():
    fulllist = []
    for file in glob.glob("*96*messages"):
            print 'reading ' + file
            fullfile = (open(file).read().splitlines())
            for x in fullfile:
                if 'RPD_MPLS_LSP_CHANGE'in x and 'Sep 17' in x:
                    if 'flag' in x:
                        fulllist.append(x.split())
    print 'done reading'
    return fulllist

newpaths=read_paths()
dnsdict = {}

def convert_paths (newpaths):
 convertedpaths = []
 dnsfile = (open("/home/mkasten/configs/addresses.txt").read().splitlines())
 for x in dnsfile:
  if '96c'in x or 'ibr' in x or '96l' in x or '20lsr' in x :
   dnsdict[x.split(":")[0]] = x.split(":")[1] +" " + x.split(":")[2]
 for x in newpaths:
  z = [x[8],x[12]]
  for y in x:
   if 'flag=0x2' in y:
    rest = y.split('(',1)[0]
    z.append(dnsdict[rest])
    if rest not in dnsdict:
         try :
          a=socket.gethostbyaddr(rest)[0]
         except :
          print "Unknown : " + rest
          a=rest
         dnsdict[rest] = a.split('.',1)[0]
         dnsdict[rest] = a
         z.append(a)
         z.append(a.split('.',1)[0])
         a='None'

  convertedpaths.append(z)
 print 'done converting'
 return convertedpaths

listofresignals = convert_paths(newpaths)

filename = 'resignallists'
outputfile = open(filename,'w')

print 'starting write'
for resig in listofresignals:
 outputfile.write( ' '.join(resig) +'\n')
