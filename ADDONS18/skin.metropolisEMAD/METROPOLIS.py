# -*- coding: utf-8 -*-


import sys,urllib2,re,xbmcaddon,os,xbmc,platform,uuid,hashlib,random,xbmcgui,time
import unicodedata


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
	text = urllib2.unquote(args['text'])
except: mode,text = '',''


def mixARABIC(string):
	#if '\u' in string:
	#	string = string.decode('unicode_escape')
	#	unicode_strings=re.findall(r'\u[0-9A-F]',string)	
	#	for unicode in unicode_strings
	#		char = unichar(
	#		replace(    , char)
	string = string.decode('utf8')
	new_string = ''
	for letter in string:
		#xbmcgui.Dialog().ok(unicodedata.decomposition(letter),hex(ord(letter)))
		if ord(letter) < 256: unicode_letter = '\u00'+hex(ord(letter)).replace('0x','')
		elif ord(letter) < 4096: unicode_letter = '\u0'+hex(ord(letter)).replace('0x','')
		else: unicode_letter = '\u'+unicodedata.decomposition(letter).split(' ')[1]
		new_string += unicode_letter
	new_string = new_string.replace('\u06CC','\u0649')
	new_string = new_string.decode('unicode_escape')
	new_string = new_string.encode('utf-8')
	return new_string


def ADDON_ID_VERSION():
	addonfolder = xbmcaddon.Addon().getAddonInfo('path').decode('utf-8')
	addonfile = os.path.join(addonfolder,'addon.xml')
	with open(addonfile,'r') as f: xmlfile = f.read()
	version = re.findall('id=[\"\'](.*?)[\"\'].*?version=[\"\'](.*?)[\"\']',xmlfile,re.DOTALL|re.IGNORECASE)
	id,ver = version[0]
	return id,ver


def dummyClientID(length):
	#addon_id,addon_version = ADDON_ID_VERSION()
	hostname = platform.node()			# empc12/localhosting
	os_type = platform.system()			# Windows/Linux
	os_version = platform.release()		# 10.0/3.14.22
	os_bits = platform.machine()		# AMD64/aarch64
	#settings = xbmcaddon.Addon(id=addon_id)
	#savednode = settings.getSetting('node')
	savednode = ''
	if savednode=='':
		node = str(uuid.getnode())		# 326509845772831
		#settings.setSetting('node',node)
	else: node = savednode
	hashComponents = node+':'+hostname+':'+os_type+':'+os_version+':'+os_bits
	md5full = hashlib.md5(hashComponents).hexdigest()
	md5 = md5full[0:length]
	return md5


def SEND_ANALYTICS_EVENT():
	addon_id,addon_version = ADDON_ID_VERSION()
	website = 'METROPOLIS'
	kodi_release = xbmc.getInfoLabel("System.BuildVersion")
	kodi_version = re.findall('&&(.*?)[ -]','&&'+kodi_release,re.DOTALL)
	kodi_version = str(float(kodi_version[0]))
	randomNumber = str(random.randrange(111111111111,999999999999))
	try:
		headers = {'User-Agent':''}
		url = 'http://www.google-analytics.com/collect?v=1&tid=UA-127045104-5&cid='+dummyClientID(32)+'&t=event&sc=end&ec='+addon_version+'&av='+addon_version+'&an=ARABIC_VIDEOS&ea='+website+'&el='+kodi_version+'&z='+randomNumber
		request = urllib2.Request(url=url,headers=headers)
		response = urllib2.urlopen(request)
		#html = response.read()
		xbmc.log('skin.metropolisEMAD ========= Sent analytics',level=xbmc.LOGNOTICE)	
	except: pass
	return


def BUSY_DIALOG(job):
	# dialog = 'busydialog'				# KODI 17.9 and earlier
	dialog = 'busydialognocancel'		# KODI 18 and later
	if job=='start': xbmc.executebuiltin('ActivateWindow('+dialog+')')
	elif job=='stop': xbmc.executebuiltin('Dialog.Close('+dialog+')')
	return


if mode==0 and text!='':
	# searching arabic text
	text = mixARABIC(text)
	text = text.decode('utf8').encode('utf8')
	window_id = 10103
	window = xbmcgui.Window(window_id)
	window.getControl(311).setLabel(text)

elif mode==1: SEND_ANALYTICS_EVENT()

elif mode in [2,3]:
	# change kodi language
	BUSY_DIALOG('start')
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
	BUSY_DIALOG('stop')





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


