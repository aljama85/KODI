# -*- coding: utf-8 -*-

import sys,urllib2,xbmcgui,unicodedata

#import traceback,xbmc,xbmcplugin,json

#xbmc.log('EMAD111::   '+str(sys.argv), level=xbmc.LOGNOTICE)


#mode = int(sys.argv[1])
#text = sys.argv[2]
#xbmc.log('EMAD222::   mode: ['+str(mode)+']     text: ['+text+']', level=xbmc.LOGNOTICE)


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


#xbmcgui.Dialog().ok('args',str(args))


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


if mode==0 and text!='':
	text = mixARABIC(text)
	text = text.decode('utf8').encode('utf8')
	window_id = 10103
	#xbmc.log('EMAD222::   window_id: ['+str(window_id)+']', level=xbmc.LOGNOTICE)
	window = xbmcgui.Window(window_id)
	window.getControl(311).setLabel(text)
	#xbmc.log('EMAD333::   text: ['+text+']', level=xbmc.LOGNOTICE)



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


"""
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


