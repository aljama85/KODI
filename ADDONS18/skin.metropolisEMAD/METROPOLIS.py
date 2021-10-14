# -*- coding: utf-8 -*-


import sys,urllib,re,os,xbmc,uuid,random,xbmcgui,time,unicodedata,xbmcvfs


kodi_release = xbmc.getInfoLabel("System.BuildVersion")
kodi_version = re.findall('&&(.*?)[ -]','&&'+kodi_release,re.DOTALL)
kodi_version = float(kodi_version[0])


if kodi_version>19:
	loglevel = xbmc.LOGINFO
	from urllib.parse import quote as _quote
	from urllib.parse import unquote as _unquote
	xbmcfolder = xbmcvfs.translatePath('special://xbmc')
	userfolder = xbmcvfs.translatePath('special://home')
else:
	loglevel = xbmc.LOGNOTICE
	from urllib import quote as _quote
	from urllib import unquote as _unquote
	xbmcfolder = xbmc.translatePath('special://xbmc')
	userfolder = xbmc.translatePath('special://home')


xbmcaddonsfolder = os.path.join(xbmcfolder,'addons')
useraddonsfolder = os.path.join(userfolder,'addons')


try:
	args = {'mode':'','text':''}
	line = sys.argv[2]
	if '?' in line:
		params = line[1:].split('&')
		for param in params:
			key,value = param.split('=',1)
			args[key] = value
	mode = args['mode']
	if mode.isdigit(): mode = int(mode)
	text = _unquote(args['text'])
except: mode,text = '',''


def mixARABIC(string):
	#if '\u' in string:
	#	string = string.decode('unicode_escape')
	#	unicode_strings=re.findall(r'\u[0-9A-F]',string)	
	#	for unicode in unicode_strings
	#		char = unichar(
	#		replace(    , char)
	#if isinstance(string,bytes): string = string.decode('utf8')
	new_string = ''
	if kodi_version<19: string = string.decode('utf8')
	import unicodedata
	for letter in string:
		#DIALOG_OK('','',unicodedata.decomposition(letter),hex(ord(letter)))
		if ord(letter) < 256: unicode_letter = '\\u00'+hex(ord(letter)).replace('0x','')
		elif ord(letter) < 4096: unicode_letter = '\\u0'+hex(ord(letter)).replace('0x','')
		else: unicode_letter = '\\u'+unicodedata.decomposition(letter).split(' ')[1]
		new_string += unicode_letter
	new_string = new_string.replace('\\u06CC','\\u0649')
	if kodi_version<19: new_string = new_string.decode('unicode_escape').encode('utf8')
	else: new_string = new_string.encode('utf8').decode('unicode_escape')
	return new_string


def dummyClientID(length):
	length = 16
	#length = length//2
	import uuid
	node = str(uuid.getnode())
	node = re.findall('[0-9]+',node,re.DOTALL)
	if node: node = node[0]
	else: node = ''
	node = length*'0'+node
	node = node[-length:]
	mm,ss = '',''
	invert = str(int('9'*(length+1))-int(node))[-length:]
	for ii in list(range(0,length,4)):
		nn = invert[ii:ii+4]
		mm += nn+'-'
		ss += str(sum(map(int,node[ii:ii+4]))%10)
	client_id = mm+ss
	return client_id


def OPENURL_SIMPLE(url):
	import urllib.request
	req = urllib.request.Request(url)
	req.add_header('User-Agent','')
	response = urllib.request.urlopen(req)
	html = response.read()
	return html


def ADDON_VERSION(addon_id):
	xbmcaddonfile = os.path.join(xbmcaddonsfolder,addon_id,'addon.xml')
	useraddonfile = os.path.join(useraddonsfolder,addon_id,'addon.xml')
	xbmcfile_exist = os.path.exists(xbmcaddonfile)
	userfile_exist = os.path.exists(useraddonfile)
	if xbmcfile_exist and userfile_exist: addonfile = useraddonfile
	elif userfile_exist: addonfile = useraddonfile
	elif xbmcfile_exist: addonfile = xbmcaddonfile
	else: return ''
	ver = ''
	try:
		xmlfile = open(addonfile,'r').read()
		version = re.findall('id=[\"\'](.*?)[\"\'].*?version=[\"\'](.*?)[\"\']',xmlfile,re.DOTALL|re.IGNORECASE)
		if version: id,ver = version[0]
	except: pass
	return ver

def SEND_ANALYTICS_EVENT():
	addon_version = ADDON_VERSION('skin.metropolisEMAD')
	website = 'METROPOLIS'
	randomNumber = str(random.randrange(111111111111,999999999999))
	try:
		url = 'http://www.google-analytics.com/collect?v=1&tid=UA-127045104-5&cid='+dummyClientID(32)+'&t=event&sc=end&ec='+addon_version+'&av='+addon_version+'&an=ARABIC_VIDEOS_NEWCLIENTID&ea='+script_name+'&el='+str(kodi_version)+'&z='+randomNumber
		html = OPENURL_SIMPLE(url)
		#import urllib2
		#headers = {'User-Agent':''}
		#request = urllib2.Request(url=url,headers=headers)
		#response = urllib2.urlopen(request)
		xbmc.log('skin.metropolisEMAD ========= Sent analytics',level=loglevel)
	except: pass
	return


def DIALOG_BUSY(job):
	if kodi_version>18: dialog = 'busydialognocancel'
	else: dialog = 'busydialog'
	if job=='start': xbmc.executebuiltin('ActivateWindow('+dialog+')')
	elif job=='stop': xbmc.executebuiltin('Dialog.Close('+dialog+')')
	return


if mode==0 and text!='':
	# in Kodi 19 when using skin keyboard to write Arabic the letters will shown reversed but only in keyboard dialog
	text = mixARABIC(text)
	if kodi_version>19:
		arabic = re.findall('[ء-ي]',text,re.DOTALL)
		if arabic: text = text[::-1]
	window_id = 10103
	window = xbmcgui.Window(window_id)
	window.getControl(311).setLabel(text)
elif mode==1: SEND_ANALYTICS_EVENT()
elif mode in [2,3]:
	# change kodi language
	DIALOG_BUSY('start')
	if mode==2: addonLANG = 'resource.language.ar_sa'
	else: addonLANG = 'resource.language.en_gb'
	time.sleep(1)
	xbmc.executebuiltin('InstallAddon('+addonLANG+')')
	time.sleep(1)
	xbmc.executebuiltin('SendClick(11)')
	time.sleep(1)
	while xbmc.getCondVisibility('Window.IsActive(progressdialog)'): time.sleep(1)
	time.sleep(1)
	xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":4,"params":{"setting":"locale.language","value":"'+addonLANG+'"}}')
	DIALOG_BUSY('stop')





"""
#try:
#window = xbmcgui.Window(10103)
#	#control = window.getFocus(311)
#	#control = window.getControl(311)
#	#window.getControl(311).setLabel(keyboard)
#xbmc.log('EMAD555::   keyboard: ['+str(keyboard.decode('utf8').encode('utf8'))+']', level=xbmc.LOGNOTICE)
#xbmcplugin.addDirectoryItems(handle=handle,items=items,totalItems=len(items))
#xbmcplugin.endOfDirectory(handle)
#aa = window.getControl(311).getLabel()
#xbmc.log('EMAD666::   aa: ['+str(aa.decode('utf8').encode('utf8'))+']', level=xbmc.LOGNOTICE)
#except:
#	traceback.print_exc(file=sys.stderr)


elif mode==1:
	window_id = xbmcgui.getCurrentWindowDialogId()
	window = xbmcgui.Window(window_id)
	url = text
	window.getControl(1112).setLabel(url)
elif mode==2 and text!='':
	keyboard = text
	ttype = 'X'
	check = isinstance(keyboard, unicode)
	if check==True: ttype='U'
	new1 = str(type(keyboard))+' '+keyboard+' '+ttype+' '
	for i in range(0,len(keyboard),1):
		new1 += hex(ord(keyboard[i])).replace('0x','')+' '
	keyboard = mixARABIC(keyboard)
	ttype = 'X'
	check = isinstance(keyboard, unicode)
	if check==True: ttype = 'U'
	new2 = str(type(keyboard))+' '+keyboard+' '+ttype+' '
	for i in range(0,len(keyboard),1):
		new2 += hex(ord(keyboard[i])).replace('0x','')+' '
	#xbmcgui.Dialog().ok(new1,new2)
elif mode==3:
	keyboard = 'emad444'
	json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Input.SendText","params":{"text":"'+keyboard+'","done":false},"id":1}')
	json.loads(json_query)
	#method="Input.SendText"
	#params='{"text":"%s", "done":false}' % keyboard
	#json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "%s", "params": %s, "id": 1}' % (method, params))
"""


