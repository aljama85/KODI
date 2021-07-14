# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'http://shoofmax.com'
website0b = 'https://static.shoofmax.com'

def MAIN(mode,url):
	if mode==50: MENU()
	elif mode==51: TITLES(url)
	elif mode==52: EPISODES(url)
	elif mode==53: PLAY(url)

def MENU():
	addDir('افلام مرتبة حسب السنوات',website0a+'/movie/1/yop',51,icon)
	addDir('افلام مرتبة حسب التقييمات',website0a+'/movie/1/review',51,icon)
	addDir('افلام مرتبة حسب المشاهدات',website0a+'/movie/1/views',51,icon)
	addDir('مسلسلات مرتبة حسب السنوات',website0a+'/series/1/yop',51,icon)
	addDir('مسلسلات مرتبة حسب التقييمات',website0a+'/series/1/review',51,icon)
	addDir('مسلسلات مرتبة حسب المشاهدات',website0a+'/series/1/views',51,icon)
	xbmcplugin.endOfDirectory(addon_handle)

def TITLES(url):
	info = url.split('/')
	sort = info[ len(info)-1 ]
	page = info[ len(info)-2 ]
	type = info[ len(info)-3 ]
	if type=='movie': type1='فيلم'
	if type=='series': type1='مسلسل'
	url = website0a+'/filter-programs/'+quote(type1)+'/'+page+'/'+sort
	html = openURL(url)
	items = re.findall('"ref":(.*?),.*?"title":"(.*?)".+?"numep":(.*?),"res":"(.*?)"',html,re.DOTALL)
	count_items=0
	for id,title,episodes_number,name in items:
		count_items += 1
		img = website0b + '/img/program/' + name + '-2.jpg'
		link = website0a + '/program/' + id
		if type=='movie': addLink(title,link,53,img)
		if type=='series': addDir(title,link+'?ep='+episodes_number,52,img)
	title='صفحة '
	for count_page in range(1,13) :
		if not page==str(count_page):
			url = website0a+'/filter-programs/'+type+'/'+str(count_page)+'/'+sort
			addDir(title+str(count_page),url,51,icon)
	xbmcplugin.endOfDirectory(addon_handle)

def EPISODES(url):
	info = url.split('=')
	episodes_number = info[1]
	info = url.split('?')
	url = info[0]
	name = xbmc.getInfoLabel( "ListItem.Title" )
	img = xbmc.getInfoLabel( "ListItem.Thumb" )
	name1 = 'مسلسل '
	name2 = ' - الحلقة '
        for episode in range(1,int(episodes_number)+1):
		link = url + '?ep=' + str(episode)
		title = name1 + name + name2 + str(episode)
		addLink(title,link,53,img)
	xbmcplugin.endOfDirectory(addon_handle)

def PLAY(url):
	html = openURL(url)
	block = re.findall('intro_end(.*?)initialize',html,re.DOTALL)[0]
	#file = open('/data/emad.html', 'w')
	#file.write(url)
	#file.write('\n\n\n')
	#file.write(block)
	#file.close()
	#xbmcgui.Dialog().ok(origin_link, backup_origin_link )
	origin_link = re.findall('var origin_link = "(.*?)"',block,re.DOTALL)[0]
	backup_origin_link = re.findall('var backup_origin_link = "(.*?)"',block,re.DOTALL)[0]
	links = re.findall('origin_link\+"(.*?)"',block,re.DOTALL)
	video1 = origin_link + links[0]
	video2 = backup_origin_link + links[1]
	multiple1 = origin_link + links[2]
	multiple2 = backup_origin_link + links[3]
	count = 0
	items_url = []
	items_name = []
	items_url.append(video1)
	items_name.append('Main server with cache')
	items_url.append(video2)
	items_name.append('Backup server with cache')
	html = openURL(multiple1)
	base = multiple1.replace('variant.m3u8','')
	items = re.findall('RESOLUTION=(.*?),.*?\n(.*?)u8',html,re.DOTALL)
        for quality,link in items:
		url = base + link + 'u8'
		count += 1
		items_url.append(url)
		items_name.append('Main server: '+quality)
	count += 1
	html = openURL(multiple2)
	base = multiple2.replace('variant.m3u8','')
	items = re.findall('RESOLUTION=(.*?),.*?\n(.*?)u8',html,re.DOTALL)
        for quality,link in items:
		url = base + link + 'u8'
		count += 1
		items_url.append(url)
		items_name.append('Backup server: '+quality)
	count += 1
	selection = xbmcgui.Dialog().select('Select Video Quality:', items_name)
	if selection == -1 : return
	url = items_url[selection]
	#url = utf8(url)
	#xbmcgui.Dialog().ok(url,'' )
	play_item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(addon_handle, True, play_item)
	#url = 'https://shoofmax.b-cdn.net/ard-alnifaq/ep1/360p/index.m3u8'
	#url = 'https://shoofmax.b-cdn.net/ard-alnifaq/ep1/fallback.mp4'
	#PLAY_OLD(url)



