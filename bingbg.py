#!/bin/python

import re, urllib, os
from config import conf

def getimg(FILE):
  f=open(FILE,'r')
  cont=f.read()
  os.remove('.temp')
  s=re.search(r"g_img={\w*url\:\'(.*\.jpg)\'.*id\:\'bgDiv\',",cont)
  if not s:
    print "Sorry, there was some problems, please try again later."
    return
  img='http://bing.com'
  img+=s.group(1)
  try:
    img=getres(img)
  except:
    return
  name=img.split('/')[-1]
  path=checkpath(name)
  if path:
    print "Downloading",name
    urllib.urlretrieve(img,path)
    print "Done. Go check it out."


def getres(img):
  s=re.search(r'_(\d\d\d\d*x\d\d\d\d*)',img)
  if not s:
    print "There was an error"
    raise
  img2=img.replace(s.group(1),conf['res'])
  try:
    f=urllib.urlopen(img2)
    return img2
  except:
    return img

def checkpath(name):
  if os.path.isdir(conf['des']):
    if os.path.isfile(conf['des']+name):
      print "Nothing new. See ya later."
      return False
    else:
      return conf['des']+name
  else:
    print "The given directory doesn't exist or you do no have the write permissions."
    print "Downloading to your home/Pictures directory."
    return '~/Pictures/'+name

if __name__=='__main__':
  print "Asking Bing if it has anything new for me..."
  try:
    urllib.urlretrieve('http://bing.com','.temp')
  except:
    print "Sorry man, couldn't reach Bing. Something wrong with your connection?"
  getimg('.temp')
