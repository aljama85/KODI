# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'http://www.panet.co.il'
website0b = 'http://m.panet.co.il'

def MAIN(mode,url):
	if mode==30: MENU()
	elif mode==31: CATEGORIES(url)
	elif mode==32: ITEMS(url)
	elif mode==33: PLAY(url)
	elif mode==34: SEARCH(url)

def MENU():
	addDir('افلام',website0a+'/movies',32,icon)
	addDir('افلام مصنفة',website0a+'/movies',31,icon)
	addDir('مسلسلات مصنفة',website0a+'/series',31,icon)
	addDir('مسرحيات',website0a+'/movies/genre/4/1',32,icon)
	addDir('بحث افلام',website0a+'/search/result/title/movies',34,icon)
	addDir('بحث مسلسلات',website0a+'/search/result/title/series',34,icon)
	xbmcplugin.endOfDirectory(addon_handle)

def CATEGORIES(url):
	info = url.split('/')
	type = info[3]
	#xbmcgui.Dialog().ok(type, url)
	if type=='series':
		html = openURL(url)
		html_blocks=re.findall('categoriesMenu(.*?)seriesForm',html,re.DOTALL)
		block= html_blocks[0]
		items=re.findall('href="(.*?)">(.*?)<',block,re.DOTALL)
		for link,name in items:
			url = website0a + link
			name = name.replace('  ','')
			addDir(name,url,32,icon)
	if type=='movies':
		html = openURL(url)
		html_blocks=re.findall('moviesGender(.*?)select',html,re.DOTALL)
		block = html_blocks[0]
		items=re.findall('option><option value="(.*?)">(.*?)<',block,re.DOTALL)
		for value,name in items:
			url = website0a + '/movies/genre/' + value
			addDir(name,url,32,icon)
		html_blocks=re.findall('moviesActor(.*?)select',html,re.DOTALL)
		block = html_blocks[0]
		items=re.findall('option><option value="(.*?)">(.*?)<',block,re.DOTALL)
		for value,name in items:
			url = website0a + '/movies/actor/' + value
			addDir(name,url,32,icon)
	xbmcplugin.endOfDirectory(addon_handle)

def ITEMS(url):
	html = openURL(url)
	type = url.split('/')[3]
	if 'home' in url: type='episodes'
	if type=='series':
		html_blocks = re.findall('panet-thumbnails(.*?)panet-pagination',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('href="(.*?)""><img src="(.*?)".*?h2>(.*?)<',block,re.DOTALL)
		for link,img,name in items:
			url = website0a + link 
			name = name.replace('  ','')
			addDir(name,url,32,img)
	if type=='movies':
		html_blocks = re.findall('panet-mars-adv-panel.*?advBarMars(.+?)panet-pagination',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('panet-thumbnail.*?href="(.*?)"><img src="(.*?)" alt="(.+?)"',block,re.DOTALL)
		for link,img,name in items:
			url = website0a + link
			addLink(name,url,33,img)
	if type=='episodes':
		page = url.split('/')[-1]
		#xbmcgui.Dialog().ok(url,'')
		if page=='1':
			html_blocks = re.findall('panet-mars-adv-panel(.+?)advBarMars',html,re.DOTALL)
			block = html_blocks[0]
			items = re.findall('panet-thumbnail.*?href="(.*?)"><img src="(.*?)".*?panet-title">(.*?)</div.*?panet-info">(.*?)</div',block,re.DOTALL)
			count = 0
			for link,img,episode,title in items:
				count += 1
				if count==10: break
				name = title + ' - ' + episode
				url = website0a + link
				addLink(name,url,33,img)
		html_blocks = re.findall('panet-mars-adv-panel.*?advBarMars(.+?)panet-pagination',html,re.DOTALL)
		block = html_blocks[0]
		items = re.findall('panet-thumbnail.*?href="(.*?)""><img src="(.*?)".*?panet-title"><h2>(.*?)</h2.*?panet-info"><h2>(.*?)</h2',block,re.DOTALL)
		for link,img,title,episode in items:
			episode = episode.replace('  ','')
			title = title.replace('  ','')
			name = title + ' - ' + episode
			url = website0a + link
			addLink(name,url,33,img)
	html_blocks = re.findall('glyphicon-chevron-right(.+?)data-revive-zoneid="4"',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('<li><a href="(.*?)">(.*?)<',block,re.DOTALL)
	for link,page in items:
		url = website0a + link 
		name = 'صفحة ' + page
		addDir(name,url,32,icon)
	xbmcplugin.endOfDirectory(addon_handle)

def PLAY(url):
	#xbmcgui.Dialog().ok(url,'')
	#url = url.replace(website0a,website0b)

	if 'series' in url:
		url = website0a + '/series/v1/seriesLink/' + url.split('/')[-1]
		html = openURL(url)
		items = re.findall('url":"(.*?)"',html,re.DOTALL)
		url = items[0]
		url = url.replace('\/','/')
	else:
		html = openURL(url)
		#items = re.findall('article-player.*?url="(.*?)".*?article-player',html,re.DOTALL)
		items = re.findall('contentURL" content="(.*?)"',html,re.DOTALL)
		url = items[0]
	play_item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(addon_handle, True, play_item)

	#xbmcgui.Dialog().ok(url,html)
	#url = 'http://vod-movies.panet.co.il/7mate-bt7bne/1.mp4'
	#item = xbmcgui.ListItem('test', iconImage=icon, thumbnailImage=icon)
	#item.setInfo(type='Video', infoLabels={ "Title": 'test'})
	#xbmc.Player().play(url, item)

def SEARCH(url):
	type=url.split('/')[-1]
	search =''
	keyboard = xbmc.Keyboard(search, 'Search')
	keyboard.doModal()
	if keyboard.isConfirmed(): search = keyboard.getText()
	if len(search)<2: return
	search = search.replace(' ','-')
	new_search = utf8(search)
	data = 'query='+new_search+'&searchDomain='+type
	html = openURL(website0a+'/search',data)
	#xbmcgui.Dialog().ok(html, new_search)
	items=re.findall('title":"(.*?)".*?link":"(.*?)"',html,re.DOTALL)
	for title,link in items:
		url = website0a + link.replace('\/','/')
		#xbmcgui.Dialog().ok(title, url.split('/')[-1]   )
		if type=='movies': addLink(title,url,33,icon)
		else: addDir(title,url+'/1',32,icon)
	xbmcplugin.endOfDirectory(addon_handle)

