# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'http://ar.ifilmtv.com'
website0b = 'http://en.ifilmtv.com'
website0c = 'http://fa.ifilmtv.com'
website0d = 'http://fa2.ifilmtv.com'

def MAIN(mode,url,page):
	if mode==20: LANGUAGE()
	elif mode==21: MENU(url)
	elif mode==22: TITLES(url,page)
	elif mode==23: EPISODES(url,page)
	elif mode==24: PLAY(url)
	elif mode==25: MUSIC_MENU(url)

def LANGUAGE():
	addDir('عربي',website0a,21,icon,101)
	addDir('English',website0b,21,icon,101)
	addDir('فارسى',website0c,21,icon,101)
	addDir('فارسى 2',website0d,21,icon,101)
	xbmcplugin.endOfDirectory(addon_handle)

def MENU(url):
	menu=['Series', 'Program', 'Music']
	website0 = SITE(url)
	html = openURL(url)
	html_blocks=re.findall('main-body.*?menu(.*?)nav',html,re.DOTALL)
	block = html_blocks[0]
	items=re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		if any(value in link for value in menu):
			url = website0 + link
			if 'Series' in link: addDir(title+' 1',url,22,icon,101)
			elif 'Music' in link: addDir(title,url,25,icon,101)
			else: addDir(title,url,22,icon,101)
			if 'Series' in link: addDir(title+' 2',url,22,icon,201)
	xbmcplugin.endOfDirectory(addon_handle)

def MUSIC_MENU(url):
	website0 = SITE(url)
	html = openURL(url)
	html_blocks = re.findall('Music-tools-header(.*?)Music-body',html,re.DOTALL)
	block = html_blocks[0]
	title = re.findall('<p>(.*?)</p>',block,re.DOTALL)[0]
	addDir(title,url,22,icon,101)
	items = re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,title in items:
		link = website0 + link
		addDir(title,link,23,icon,101)
	xbmcplugin.endOfDirectory(addon_handle)

def TITLES(url,page):
	website0 = SITE(url)
	lang = LANG(url)
	info = url.split('/')
	type = info[ len(info)-2 ]
	#xbmcgui.Dialog().ok(url, website0)
	order = str(int(page)/100)
	page = str(int(page)%100)
	#xbmcgui.Dialog().ok(page, order)
	count_items=0
	if type=='Series': category='3'
	if type=='Film': category='5'
	if type=='Program': category='7'
	if type=='Series' or type=='Film' or type=='Program':
		url2 = website0+'/Home/PageingItem?category='+category+'&page='+page+'&size=30&orderby='+order
		html = openURL(url2)
		items = re.findall('"Id":(.*?),"Title":(.*?),.+?"ImageAddress_S":"(.*?)"',html,re.DOTALL)
		for id,title,img in items:
			title = title.replace('\\','')
			title = title.replace('"','')
			count_items += 1
			link = website0 + '/' + type + '/Content/' + id
			img = website0 + quote(img)
			addDir(title,link,23,img,order+'01')
	if type=='Music':
		html = openURL(website0+'/Music/Index?page='+page)
		html_blocks = re.findall('pagination-demo(.*?)pagination-demo',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>',block,re.DOTALL)
		for link,img,title in items:
			count_items += 1
			img = website0 + img
			link = website0 + link
			addDir(title,link,23,img,101)
	if count_items>20:
		title='صفحة '
		if lang=='en': title = ' Page '
		if lang=='fa': title = ' صفحه '
		if lang=='da': title = ' صفحه '
		for count_page in range(1,11) :
			if not page==str(count_page):
				counter = '0'+str(count_page)
				addDir(title+str(count_page),url,22,icon,order+counter[-2:])
	xbmcplugin.endOfDirectory(addon_handle)

def EPISODES(url,page):
	website0 = SITE(url)
	lang = LANG(url)
	info = url.split('/')
	id = info[ len(info)-1 ]
	type = info[ 3 ]
	order = str(int(page)/100)
	page = str(int(page)%100)
	count_items=0
	#xbmcgui.Dialog().ok(url, type)
	if type=='Series':
		html = openURL(url)
		items = re.findall('Comment_panel_Item.*?p>(.*?)<i.+?var inter_ = (.*?);.*?src="(.*?)\'.*?data-url="(.*?)\'',html,re.DOTALL)
		title = ' - الحلقة '
		if lang=='en': title = ' - Episode '
		if lang=='fa': title = ' - قسمت '
		if lang=='da': title = ' - قسمت '
		if lang=='fa': linklang = ''
		else: linklang = lang
		for name,count,img,link in items:
			for episode in range(int(count),0,-1):
				img1 = img + linklang + id + '/' + str(episode) + '.png' 
				link1 = link + linklang + id + '/' + str(episode) + '.mp4' 
				name = name.replace('&quot;','')
				name1 = name + title + str(episode)
				addLink(name1,link1,24,img1)
	if type=='Program':
		url2 = website0+'/Home/PageingAttachmentItem?id='+str(id)+'&page='+page+'&size=30&orderby=1'
		html = openURL(url2)
		items = re.findall('Episode":(.*?),.*?ImageAddress_S":"(.*?)".*?VideoAddress":"(.*?)".*?Discription":"(.*?)".*?Caption":"(.*?)"',html,re.DOTALL)
		title = ' - الحلقة '
		if lang=='en': title = ' - Episode '
		if lang=='fa': title = ' - قسمت '
		if lang=='da': title = ' - قسمت '
		for episode,img,link,desc,name in items:
			count_items += 1
			img1 = website0 + quote(img)
			link1 = website0 + quote(link) 
			if desc=='': name1 = name + title + str(episode)
			else: name1 = name + title + str(episode) + ' - ' + desc
			addLink(name1,link1,24,img1)
	if type=='Music':
		if 'Content' in url and 'category' not in url:
			url2 = website0+'/Music/GetTracksBy?id='+str(id)+'&page='+page+'&size=30&type=0'
			html = openURL(url2)
			#xbmcgui.Dialog().ok(url2, str(len(html)) )
			items = re.findall('ImageAddress_S":"(.*?)".*?VoiceAddress":"(.*?)".*?Caption":"(.*?)","Title":"(.*?)"',html,re.DOTALL)
			for img,link,name,title in items:
				count_items += 1
				img1 = website0 + quote(img)
				link1 = website0 + quote(link)
				name1 = name + ' - ' + title
				name1 = name1.strip(' ')
				name1 = name1.decode('unicode_escape')
				addLink(name1,link1,24,img1)
		elif 'Clips' in url:
			html = openURL(website0+'/Music/GetTracksBy?id=0&page='+page+'&size=30&type=15')
			items = re.findall('ImageAddress_S":"(.*?)".*?Caption":"(.*?)".*?VideoAddress":"(.*?)"',html,re.DOTALL)
			for img,title,link in items:
				count_items += 1
				img1 = website0 + quote(img)
				link1 = website0 + quote(link)
				#title1 = title.replace('  ','')
				title1 = title.strip(' ')
				addLink(title1,link1,24,img1)
		elif 'category' in url:
			if 'category=6' in url:
				html = openURL(website0+'/Music/GetTracksBy?id=0&page='+page+'&size=30&type=6')
			elif 'category=4' in url:
				html = openURL(website0+'/Music/GetTracksBy?id=0&page='+page+'&size=30&type=4')
			items = re.findall('ImageAddress_S":"(.*?)".*?VoiceAddress":"(.*?)".*?Caption":"(.*?)","Title":"(.*?)"',html,re.DOTALL)
			for img,link,name,title in items:
				count_items += 1
				img1 = website0 + quote(img)
				link1 = website0 + quote(link)
				name1 = name + ' - ' + title
				name1 = name1.strip(' ')
				#name1 = name1.replace('  ','')
				addLink(name1,link1,24,img1)
	if type=='Music' or type=='Program':
		if count_items>25:
			title='صفحة '
			if lang=='en': title = ' Page '
			if lang=='fa': title = ' صفحه '
			if lang=='da': title = ' صفحه '
			for count_page in range(1,11):
				if not page==str(count_page):
					counter = '0'+str(count_page)
					addDir(title+str(count_page),url,23,icon,order+counter[-2:])
	xbmcplugin.endOfDirectory(addon_handle)

def PLAY(url):
	#xbmcgui.Dialog().ok(url, str(addon_handle)
	play_item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(addon_handle, True, play_item)
	
def SITE(url):
	if website0a in url: site = website0a
	elif website0b in url: site = website0b
	elif website0c in url: site = website0c
	elif website0d in url: site = website0d
	return site

def LANG(url):
	if website0a in url: lang = 'ar'
	elif website0b in url: lang = 'en'
	elif website0c in url: lang = 'fa'
	elif website0d in url: lang = 'da'
	return lang

