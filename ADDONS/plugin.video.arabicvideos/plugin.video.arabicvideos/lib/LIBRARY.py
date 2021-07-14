# -*- coding: utf-8 -*-
import urllib2,xbmcplugin,xbmcgui,sys,xbmc,os,unicodedata,re,time

addon_handle = int(sys.argv[1])
addon_id = sys.argv[0].split('/')[2]
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

def addLink(name,url,mode,iconimage,duration=''):
	#xbmcgui.Dialog().ok(duration,'')
	u='plugin://'+addon_id+'/?mode='+str(mode)+'&url='+quote(url)
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo('Video', {'mediatype': 'video'})
	if duration != '' :
		if len(duration)<=2 : duration = '00:' + duration
		if len(duration)<=5 : duration = '00:' + duration
		duration = sum(x * int(t) for x, t in zip([3600,60,1], duration.split(":"))) 	
		liz.setInfo('Video', {'duration': duration})
	liz.setProperty('IsPlayable', 'true')
	xbmcplugin.setContent(addon_handle, 'videos')
	xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz,isFolder=False)

def openURL(url,data=''):
	html = ''
	start = time.time()
	if data=='': request = urllib2.Request(url)
	else: request = urllib2.Request(url,data=data)

	#http.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	#http.add_header('Referer',' http://www.panet.co.il/Ext/players/flv5/player.swf')
	#http.add_header('Accept',' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	#http.add_header('Host',' fms-eu0.panet.co.il')
	#http.add_header('Accept-Language',' en-US,en;q=0.5')
	#http.add_header('Accept-Encoding', 'deflate')
	#http.add_header('Cookie',' __auc=82d7ffe213cb1b4ce1d273c7ba1; __utma=31848767.848342890.1360191082.1360611183.1360620657.4; __utmz=31848767.1360191082.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=31848767.4.10.1360620660; __utmc=31848767; __asc=169c084d13ccb4fa36df421055e')
	#http.add_header('Connection',' keep-alive')

	#http.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
	#http.add_header('Connection', 'close')
	#http.add_header('Connection', 'keep-alive')
	try:
		http = urllib2.urlopen(request)
		html = http.read()
		#xbmcgui.Dialog().ok(url,html)
		end = time.time()
		#if end-start > 4 : xbmcgui.Dialog().notification('slower than 4 sec', str(end-start) )
	except:
		select = xbmcgui.Dialog().yesno('No Data or Slow Internet !', 'Try again?')
		if select==True: openURL(url)

        #file = open('/data/emad.html', 'w')
        #file.write(url)
	#file.write('\n\n\n')
        #file.write(html)
        #file.close()

	return html

def quote(url):
	return urllib2.quote(url,':/')

def addDir(name,url='',mode='',iconimage=icon,page='',category=''):
	u='plugin://'+addon_id+'/?mode='+str(mode)
	if url != '' : u = u + '&url=' + quote(url)
	if page != '' : u = u + '&page=' + str(page)
	if category != '' : u = u + '&category=' + str(category)
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('fanart_image', fanart)
	xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz,isFolder=True)

def AAAutf8(string):
	if '\u' in string : string = string.decode('unicode_escape')
	string = string.encode('utf-8')
	return string

def utf8(string):
	#if '\u' in string:
	#	string = string.decode('unicode_escape')
	#	unicode_strings=re.findall(r'\u[0-9A-F]',string)	
	#	for unicode in unicode_strings
	#		char = unichar(
	#		replace(    , char)
	string = string.decode('utf8')
	new_string = ''
	for letter in string:
		if ord(letter) < 128: unicode_letter = '\u00'+hex(ord(letter)).replace('0x','')
		else: unicode_letter = '\u'+unicodedata.decomposition(letter).split(' ')[1]
		new_string += unicode_letter
	new_string = new_string.decode('unicode_escape')
	new_string = new_string.encode('utf-8')
	return new_string


#xbmcgui.Dialog().ok('test','')


def PLAY_FROM_DIRECTORY(url):
	url=url.decode('unicode_escape')
	url=url.replace(' ','%20')
	###if '%' not in url: url = quote(url)
	title = xbmc.getInfoLabel('ListItem.Title')
	play_item = xbmcgui.ListItem(title)
	xbmc.Player().play(url, play_item)

def PLAY_OLD(url):
	title = 'testing'
	play_item = xbmcgui.ListItem( title, iconImage=icon, )
	play_item.setInfo( "video", { "Title": title } )
	#playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	#playlist.clear()
	#playlist.add( url, play_item )
	#xbmc.Player().play(playlist,play_item)
	xbmc.Player().play(url,play_item)


