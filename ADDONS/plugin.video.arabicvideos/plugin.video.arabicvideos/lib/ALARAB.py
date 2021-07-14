# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'http://tv.alarab.com'
website0b = 'http://tv1.alarab.com'
website0c = 'http://vod.alarab.com'

def MAIN(mode,url):
	#return
	if mode==10: MENU()
	elif mode==11: ITEMS(url)
	elif mode==12: PLAY(url)
	elif mode==13: SEARCH()
	elif mode==14: LATEST()

def MENU():
	addDir('البحث عن فيديو ///',website0a,13,icon)
	addDir('مسلسلات جديدة ///',website0a,14,icon)
	html = openURL(website0a)
	html_blocks=re.findall('footer_sec(.*?)social-network',html,re.DOTALL)
	block=html_blocks[0]
	#xbmcgui.Dialog().ok(str(len(html)), str(len(block)) )
	items=re.findall('href="(.*?)".*?>(.*?)<',block,re.DOTALL)
	for url,name in items:
		url = url.replace(website0b,website0a)
		addDir(name,url,11,icon)
	xbmcplugin.endOfDirectory(addon_handle)

def LATEST():
	html = openURL(website0a)
	html_blocks=re.findall('right_content.+?heading-top(.+?)heading-top',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)".+?src="(.*?)" alt="(.*?)"',block,re.DOTALL)
	for url,img,name in items:
		url = website0a + url
		addDir(name,url,11,img)
	xbmcplugin.endOfDirectory(addon_handle)

def ITEMS(url):
	html = openURL(url)
	html_blocks = re.findall('heading-list(.*?)right_content',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('video-box.*?href="(.*?)".+?src="(.*?)" alt="(.*?)"',block,re.DOTALL)
	for link,img,name in items:
		url = website0a + link
		if 'series' in link:
			addDir(name,url,11,img)
		else:
			addLink(name,url,12,img)
	items = re.findall('tsc_3d_button red.*?href="(.*?)" title="(.*?)"',block,re.DOTALL)
	for link,page in items:
		url = website0a + link
		addDir(page,url,11,icon)
	xbmcplugin.endOfDirectory(addon_handle)

def PLAY(url):
	id = re.findall('/v(.+?)-',url,re.DOTALL)[0]
	url = 'http://alarabplayers.alarab.com/?vid='+id
	html = openURL(url)
	#xbmcgui.Dialog().ok(url,'')
	#progress = xbmcgui.DialogProgress()
	#progress.create('Opening website')
	#progress.update(25,'Finding videos')
	#progress.update(50,'','Getting Links')
	#progress.update(75,'','','Playing now')
	#progress.close()
	#xbmcgui.Dialog().ok('Finding videos', url)
	#xbmcgui.Dialog().notification('Finding videos','')
	#file = open('/data/emad.html', 'w')
	#file.write(url)
	#file.write('\n\n\n')
	#file.write(html)
	#file.close()
	html_blocks = re.findall('playerInstance.setup(.+?)primary',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('file: "(.*?)".+?label: "(.*?)"',block,re.DOTALL)
	if items: 
		count = 0
		items_url = []
		items_name = []
		for file,label in reversed(items):
			count += 1
			items_url.append(file)
			items_name.append(label)
		if count > 1:
			selection = xbmcgui.Dialog().select('Select Video Quality:', items_name)
			#xbmcgui.Dialog().ok(items_name[selection], items_url[selection])
			if selection == -1 : return
		else:
			selection = 0
		url = items_url[selection]
		url = utf8(url)
	else:
		items = re.findall('file:"(.*?)"',block,re.DOTALL)
		if items:
			url = 'http:' + items[0]
			if 'youtu' in url:
				youtubeID = url.split('=')[1]
				url = 'plugin://plugin.video.youtube/play/?video_id='+youtubeID
		else:
			#if not 'alarabplayers' in url:
			#	links = re.findall('iframe src="(.*?)"',html,re.DOTALL)
			#	link = links[0]
			#	url = link.split('&')[0]
			#	PLAY(url)
			#	return
			#else:
			xbmcgui.Dialog().notification('No video file found','')
			return
	play_item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(addon_handle, True, play_item)

def SEARCH():
	search =''
	keyboard = xbmc.Keyboard(search, 'Search')
	keyboard.doModal()
	if keyboard.isConfirmed(): search = keyboard.getText()
	if len(search)<2: return
	search = search.replace(' ','-')
	new_search = utf8(search)
	searchlink = website0a + "/q/" + new_search
	ITEMS(searchlink)

