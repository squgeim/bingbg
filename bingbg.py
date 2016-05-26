#!/usr/bin/python2

import re, os, urllib
from config import conf
from bs4 import BeautifulSoup
import cssutils
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

class bingBg():
  
  def __init__(self):
    html = self.get_html()
    self.img_url = self.get_image_url(html)
    self.download_dir = self.get_directory()
  
  def has_new(self):
    if os.path.isfile( self.get_directory() + self.get_image_name() ):
      return False
    else:
      return True
      
  def download_image(self):
    urllib.urlretrieve( self.img_url, self.download_dir + self.get_image_name() )
    
  def get_html(self):
    '''
      TODO: get phantomjs to work
    '''
    wd = webdriver.Firefox()
    #wd = webdriver.PhantomJS()
    wd.get('https://bing.com')
    WebDriverWait(wd, 5)
    temp = wd.page_source
    wd.quit()
    return temp
    
  def get_image_url(self, html):
    soup = BeautifulSoup(html, 'html.parser')
    bgDiv = soup.find('div', {'id':'bgDiv'})
    divStyle = cssutils.parseString('.div {' + str(bgDiv['style']) + '}')
    image = divStyle.cssRules[0].style.backgroundImage
    s = re.search(r'url\((.*\.jpg)\)', image)
    if not s:
      raise Exception('Couldn\'t parse html.')
    url = s.group(1)
    try:
      url = self.getres(url)
    except:
      raise Exception('Can\'t parse filename.')
    return url
    
  def get_image_name(self):
    return self.img_url.split('/')[-1]
    
  def getres(self, img):
    s=re.search(r'_(\d\d\d\d*x\d\d\d\d*)',img)
    if not s:
      raise
    img2=img.replace(s.group(1),conf['res'])
    try:
      f=urllib.urlopen(img2)
      return img2
    except:
      return img
      
  def get_directory(self):
    if os.path.isdir(conf['des']):
      return conf['des']
    else:
      return '~/Pictures/'
      
if __name__ == '__main__':
  print "Asking Bing if it has anything new for me..."
  try:
    app = bingBg()
    if not app.has_new():
      print 'Nothing new. See ya later.'
    else:
      print 'Downloading ' + app.get_image_name() + '...'
      app.download_image()
      print 'Done. Go check it out.'
  except:
    print 'There was a problem reaching Bing.'
      