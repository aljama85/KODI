# -*- coding: utf-8 -*-
import urllib2,xbmcplugin,sys

from lib.LIBRARY import *

def MAIN():
	website1 = 'موقع كل العرب'
	website2 = 'موقع قناة اي فيلم'
	website3 = 'موقع بانيت'
	website4 = 'موقع قناة المعارف'
	website5 = 'موقع شوف ماكس'
	addDir(website5,'',50)
	addDir(website1,'',10)
	addDir(website3,'',30)
	addDir(website2,'',20)
	addDir(website4,'',40)
	xbmcplugin.endOfDirectory(addon_handle)

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

url=''
mode=''
page=''
category=''
params=get_params()
try: mode=int(params["mode"])
except: pass
try: url=urllib2.unquote(params["url"])
except: pass
try: page=int(params["page"])
except: pass
try: category=params["category"]
except: pass
try: keyboard=params["keyboard"]
except: pass

if mode=='': MAIN()
if mode>=0 and mode<=9: from lib.KEYBOARD import MAIN ; MAIN(mode,keyboard)
if mode>=10 and mode<=19: from lib.ALARAB import MAIN ; MAIN(mode,url)
if mode>=20 and mode<=29: from lib.IFILM import MAIN ; MAIN(mode,url,page)
if mode>=30 and mode<=39: from lib.PANET import MAIN ; MAIN(mode,url)
if mode>=40 and mode<=49: from lib.ALMAAREF import MAIN ; MAIN(mode,url,category)
if mode>=50 and mode<=59: from lib.SHOOFMAX import MAIN ; MAIN(mode,url)




