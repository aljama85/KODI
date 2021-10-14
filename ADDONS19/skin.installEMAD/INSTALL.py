# -*- coding: utf-8 -*-


import sys,re,xbmcaddon,os,xbmc,uuid,random,xbmcgui,time,threading,xbmcvfs


kodi_release = xbmc.getInfoLabel("System.BuildVersion")
kodi_version = re.findall('&&(.*?)[ -]','&&'+kodi_release,re.DOTALL)
kodi_version = float(kodi_version[0])


xbmcfolder = xbmcvfs.translatePath('special://xbmc')
xbmcaddonsfolder = os.path.join(xbmcfolder,'addons')
userfolder = xbmcvfs.translatePath('special://home')
useraddonsfolder = os.path.join(userfolder,'addons')


if kodi_version>19:
	loglevel = xbmc.LOGINFO
	addons_dbfile = os.path.join(userfolder,'userdata','Database','Addons33.db')
else:
	loglevel = xbmc.LOGNOTICE
	addons_dbfile = os.path.join(userfolder,'userdata','Database','Addons27.db')


def HIGEST_REPOSITORIES_VERSION():
	ver1 = ADDON_VERSION('repository.emad')
	#ver2 = ADDON_VERSION('repository.emad.github')
	#ver3 = ADDON_VERSION('repository.emad.gitea')
	#ver4 = ADDON_VERSION('repository.emad.codeberg')
	#max_ver = max(ver1,ver2,ver3,ver4)
	max_ver = ver1
	return max_ver


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


def SEND_ANALYTICS_EVENT():
	addon_version = ADDON_VERSION('skin.installEMAD')
	script_name = 'INSTALL'
	randomNumber = str(random.randrange(111111111111,999999999999))
	try:
		url = 'http://www.google-analytics.com/collect?v=1&tid=UA-127045104-5&cid='+dummyClientID(32)+'&t=event&sc=end&ec='+addon_version+'&av='+addon_version+'&an=ARABIC_VIDEOS_NEWCLIENTID&ea='+script_name+'&el='+str(kodi_version)+'&z='+randomNumber
		html = OPENURL_SIMPLE(url)
		#import urllib2
		#headers = {'User-Agent':''}
		#request = urllib2.Request(url=url,headers=headers)
		#response = urllib2.urlopen(request)
		xbmc.log('skin.installEMAD ========= Sent analytics',level=loglevel)
	except: pass
	return


def DIALOG_BUSY(job):
	if kodi_version>18: dialog = 'busydialognocancel'
	else: dialog = 'busydialog'
	if job=='start': xbmc.executebuiltin('ActivateWindow('+dialog+')')
	elif job=='stop': xbmc.executebuiltin('Dialog.Close('+dialog+')')
	return


def SHOW_AV_VERSION(window22,lang,version):
	if lang=='ar': text1 = text_av_ver_ar+'\n('+version+')'
	else: text1 = text_av_ver_en+'\n('+version+')'
	window22.getControl(9003).setLabel(text1)
	return


def SHOW_SKIN_VERSION(window22,lang,version):
	if lang=='ar': text2 = text_skin_ver_ar+' ('+version+')'
	else: text2 = text_skin_ver_en+' ('+version+')'
	window22.getControl(9004).setLabel(text2)
	return


def SHOW_REPOS_VERSION(window22,lang,version):
	if lang=='ar': text1 = text_repos_ver_ar+' ('+version+')'
	else: text1 = text_repos_ver_en+' ('+version+')'
	window22.getControl(9005).setLabel(text1)
	return


def UPDATE_ADDON_REPOS():
	time.sleep(1)
	xbmc.executebuiltin('UpdateAddonRepos')
	time.sleep(1)
	xbmc.log('skin.installEMAD ========= Executed UpdateAddonRepos',level=loglevel)
	return


def UPDATE_LOCAL_ADDONS():
	time.sleep(1)
	xbmc.executebuiltin('UpdateLocalAddons')
	time.sleep(1)
	xbmc.log('skin.installEMAD ========= Executed UpdateLocalAddons',level=loglevel)
	return


xbmc.log('skin.installEMAD ========= KODIEMAD Installation started',level=loglevel)
DIALOG_BUSY('start')


if 'mode=1' in sys.argv[2]:
	SEND_ANALYTICS_EVENT()
	sys.exit()


# should be before showing progressbar because it needs addons version (0.0.0.0)
addon_folder = os.path.join(userfolder,'addons','plugin.video.arabicvideos')
if not os.path.exists(addon_folder):
	addons_zipfile = os.path.join(xbmcfolder,'addons','skin.installEMAD','addons.zip')
	zipfile_contents = open(addons_zipfile,'rb').read()
	import zipfile,io
	file_like_object = io.BytesIO(zipfile_contents)
	zf = zipfile.ZipFile(file_like_object)
	zf.extractall(useraddonsfolder)
	UPDATE_LOCAL_ADDONS()
	xbmc.log('skin.installEMAD ========= Empty Addons Installed',level=loglevel)


progressbar_totaltime = 720
button0,button1,button2 = 'عربي','English','إلغاء - Quit'
textAR = 'بدأ كودي الآن تحديث نفسه وتثبيت جميع الإضافات . الرجاء الانتظار 12 دقيقة'
textEN = 'Kodi started now to update itself and install all addons . Please wait for 12 minutes'
arabic_big_text = 'برنامج كودي الإصدار رقم [COLOR FFFFFF00]('+str(kodi_version)+')[/COLOR] بدأ الآن عملية تثبيت برنامج عماد للفيديوهات العربية ومعه جلد عماد متروبولس ومعه مخزن عماد ... عند نهاية هذه العملية سوف تختفي هذه الشاشة ويظهر بدلا منها القائمة الرئيسية لبرنامج كودي ومعها برنامج عماد ... حجم التحميل المتوقع هو تقريبا 100 ميغابايت وهذه تحتاج وقت تقريبا 10 دقائق لتحميل الملفات من الأنترنيت وتثبيتها في كودي ... قد تحتاج وقت اكثر إذا الأنترنيت عندك بطيئة أو جهازك بطيء ... أهمل رسائل الخطأ في هذه الشاشة ... في حال حدوث مشكلة قم بمسح كل شيء وابدأ من جديد'
english_big_text = 'KODI software version [COLOR FFFFFF00]('+str(kodi_version)+')[/COLOR] started now the install of EMAD Arabic Videos with EMAD metropolis skin with EMAD Repositories . At the end of this process the screen will switch to KODI main menu and EMAD Arabic Videos . The download size expected is 100 MegaByte and this might need 10 minutes to download the files and install them on KODI . Slow internet or slow device will need more time . Ignore error messages in this screen . If you get problems then delete everything and start again'
text_av_ver_ar = '[COLOR FFC89008]رقم إصدار برنامج عماد في كودي:[/COLOR]'
text_av_ver_en = '[COLOR FFC89008]Version of Arabic Videos in Kodi:[/COLOR]'
text_skin_ver_ar = '[COLOR FFC89008]رقم إصدار جلد متروبولس عماد في كودي:[/COLOR]'
text_skin_ver_en = '[COLOR FFC89008]Version of skin metropolisEMAD\nin Kodi:[/COLOR]'
text_repos_ver_ar = '[COLOR FFC89008]رقم إصدار مخزن عماد في كودي:[/COLOR]'
text_repos_ver_en = '[COLOR FFC89008]Version of EMAD Repositories in Kodi:[/COLOR]'


window = xbmcgui.Window(10000)
window.getControl(9001).setLabel(arabic_big_text)
version = HIGEST_REPOSITORIES_VERSION()
SHOW_REPOS_VERSION(window,'ar',version)
version = ADDON_VERSION('plugin.video.arabicvideos')
SHOW_AV_VERSION(window,'ar',version)
version = ADDON_VERSION('skin.metropolisEMAD')
SHOW_SKIN_VERSION(window,'ar',version)
xbmc.log('skin.installEMAD ========= MainScreen and ProgressBar started',level=loglevel)


import sqlite3
conn = sqlite3.connect(addons_dbfile)
conn.text_factory = str
cc = conn.cursor()
#cc.execute('UPDATE installed SET origin = "repository.emad.github" WHERE addonID = "repository.emad.github"')
#cc.execute('UPDATE installed SET origin = "repository.emad.gitea" WHERE addonID = "repository.emad.gitea"')
#cc.execute('UPDATE installed SET origin = "repository.emad.codeberg" WHERE addonID = "repository.emad.codeberg"')
cc.execute('UPDATE installed SET origin = "repository.emad" WHERE addonID = "plugin.video.arabicvideos"')
cc.execute('UPDATE installed SET origin = "repository.emad" WHERE addonID = "skin.metropolisEMAD"')
cc.execute('UPDATE installed SET origin = "repository.emad" WHERE addonID = "repository.emad"')
conn.commit()
conn.close()
UPDATE_LOCAL_ADDONS()
xbmc.log('skin.installEMAD ========= Fixed addons auto-update',level=loglevel)


#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"repository.emad.gitea","enabled":true}}')
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"repository.emad.github","enabled":true}}')
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"repository.emad.codeberg","enabled":true}}')
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"repository.emad","enabled":true}}')
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"plugin.video.arabicvideos","enabled":true}}')
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"skin.metropolisEMAD","enabled":true}}')
UPDATE_LOCAL_ADDONS()
xbmc.log('skin.installEMAD ========= Empty addons enabled',level=loglevel)


class MyConfirmDialog(xbmcgui.WindowXMLDialog):
	def __init__(self,*args,**kwargs):
		self.controlID = -1
		self.lang = 'ar'
	def onClick(self,controlID):
		self.controlID = controlID
		if controlID==10: self.lang = 'ar'
		elif controlID==11: self.lang = 'en'
		self.close()


def updateProgressBar(dialog22,window22):
	zero = '0.0.0.0'
	addon1_ver_old,addon2_ver_old,addon3_ver_old,addon4_ver_old, = zero,zero,zero,zero
	count_old,time_old = 0,0
	count_old_2,time_old_2 = 0,0
	for ii in range(progressbar_totaltime):
		time.sleep(1)
		timeTEXT = time.strftime("%M:%S",time.gmtime(progressbar_totaltime-ii))
		header = 'وقت متبقي:   '+timeTEXT+'   :Time Remaining'
		dialog22.getControl(1).setLabel(header)
		percent = int(100*ii/progressbar_totaltime)
		dialog22.getControl(20).setPercent(percent)
		if ii==0:
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"service.xbmc.versioncheck","enabled":false}}')
			xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"screensaver.mode","value":""}}')
		elif ii%20==3:
			addon1_ver_new = HIGEST_REPOSITORIES_VERSION()
			if addon1_ver_new!=addon1_ver_old:
				addon1_ver_old = addon1_ver_new
				SHOW_REPOS_VERSION(window22,dialog22.lang,addon1_ver_new)
				xbmc.log('skin.installEMAD ========= 1st method repository.emad '+addon1_ver_new+' installed',level=loglevel)
		elif ii%20==6:
			addon2_ver_new = ADDON_VERSION('plugin.video.arabicvideos')
			if addon2_ver_new!=addon2_ver_old:
				addon2_ver_old = addon2_ver_new
				SHOW_AV_VERSION(window22,dialog22.lang,addon2_ver_new)
				xbmc.log('skin.installEMAD ========= 1st method plugin.video.arabicvideos '+addon2_ver_new+' installed',level=loglevel)
		elif ii%20==9:
			addon3_ver_new = ADDON_VERSION('skin.metropolisEMAD')
			if addon3_ver_new!=addon3_ver_old:
				addon3_ver_old = addon3_ver_new
				SHOW_SKIN_VERSION(window22,dialog22.lang,addon3_ver_new)
				xbmc.log('skin.installEMAD ========= 1st method skin.metropolisEMAD '+addon3_ver_new+' installed',level=loglevel)
		elif ii%20==12:
			addon4_ver_new = ADDON_VERSION('resource.language.ar_sa')
			if addon4_ver_new!=addon4_ver_old:
				addon4_ver_old = addon4_ver_new
				xbmc.log('skin.installEMAD ========= 1st method resource.language.ar_sa '+addon4_ver_new+' installed',level=loglevel)
		elif ii%20==15:
			count_new_2 = len(os.listdir(useraddonsfolder))
			time_new_2 = time.time()
			if count_new_2>count_old_2: count_old_2,time_old_2 = count_new_2,time_new_2
			elif 120<(time_new_2-time_old_2)<150: UPDATE_ADDON_REPOS()
		elif ii%20==18:
			count_new = len(os.listdir(useraddonsfolder))
			time_new = time.time()
			if count_new>count_old: count_old,time_old = count_new,time_new
			elif 180<(time_new-time_old)<210: break
		elif ii%20==1:
			installed = addon1_ver_old>zero and addon2_ver_old>zero and addon3_ver_old>zero and addon4_ver_old>zero
			if installed: break
		"""
		elif ii%20==0:
			try:
				if not th1.is_alive(): raise RuntimeError('Forced Error')
			except:
				seq = seq+1
				th1 = threading.Thread(target=UPDATE_REPOS,args=(seq,0,))
		"""
		'''
		files_count = 0
		addonfolder = os.path.join(useraddonsfolder,'skin.metropolisEMAD')
		for root,dirs,files in os.walk(addonfolder):
			files_count += len(files)
		#dialog22.getControl(9).setText(str(files_count))
		#time.sleep(5)
		if files_count>700: break
		'''
	header = 'وقت متبقي:   '+'00:00'+'   :Time Remaining'
	dialog22.getControl(1).setLabel(header)
	dialog22.getControl(20).setPercent(100)
	time.sleep(1)
	dialog22.controlID = 99
	dialog22.close()
	del dialog22
	return


thisaddonfolder = xbmcaddon.Addon().getAddonInfo('path')
dialog = MyConfirmDialog('DialogConfirmThreeButtons.xml',thisaddonfolder,'Default','720p')
dialog.show()
dialog.getControl(10).setLabel(button0)
dialog.getControl(11).setLabel(button1)
dialog.getControl(12).setLabel(button2)
dialog.getControl(20).setVisible(True)
dialog.getControl(9).setText(textAR)
th = threading.Thread(target=updateProgressBar,args=(dialog,window,))
th.start()
while dialog.controlID==-1:
	#if dialog.controlID==-1:
	#	xbmc.log('skin.installEMAD ========= User requested exit',level=loglevel)
	dialog.doModal()
	if dialog.controlID==10:
		xbmc.log('skin.installEMAD ========= User requested Arabic interface',level=loglevel)
		window.getControl(9001).setLabel(arabic_big_text)
		window.getControl(9002).setLabel('')
		dialog.getControl(9).setText(textAR)
		version = HIGEST_REPOSITORIES_VERSION()
		SHOW_REPOS_VERSION(window,dialog.lang,version)
		version = ADDON_VERSION('plugin.video.arabicvideos')
		SHOW_AV_VERSION(window,dialog.lang,version)
		version = ADDON_VERSION('skin.metropolisEMAD')
		SHOW_SKIN_VERSION(window,dialog.lang,version)
	elif dialog.controlID==11:
		xbmc.log('skin.installEMAD ========= User requested English interface',level=loglevel)
		window.getControl(9001).setLabel('')
		window.getControl(9002).setLabel(english_big_text)
		dialog.getControl(9).setText(textEN)
		version = HIGEST_REPOSITORIES_VERSION()
		SHOW_REPOS_VERSION(window,dialog.lang,version)
		version = ADDON_VERSION('plugin.video.arabicvideos')
		SHOW_AV_VERSION(window,dialog.lang,version)
		version = ADDON_VERSION('skin.metropolisEMAD')
		SHOW_SKIN_VERSION(window,dialog.lang,version)
	elif dialog.controlID==12:
		xbmc.log('skin.installEMAD ========= User requested Quit',level=loglevel)
		xbmc.executebuiltin('Quit()',True)
		sys.exit()
	elif dialog.controlID==99:
		xbmc.log('skin.installEMAD ========= ProgressBar closed',level=loglevel)
		break
	dialog.controlID = -1


"""
def INSTALL_ADDON(addon_id):
	#addon_ver = ADDON_VERSION(addon_id)
	if 1 or not addon_ver>'0.0.0.0':
		#UPDATE_ADDON_REPOS()
		xbmc.executebuiltin('InstallAddon('+addon_id+')')
		time.sleep(10)
		xbmc.executebuiltin('SendClick(11)')
		while xbmc.getCondVisibility('Window.IsActive(progressdialog)'): time.sleep(1)
		xbmc.log('skin.installEMAD ========= 2nd method '+addon_id+' installed',level=loglevel)
	return


# "EnableAddon" show question about install addon in kodi 19
# "InstallAddon" does not ask the question in kodi 19
#xbmc.executebuiltin('EnableAddon("repository.emad")')
#xbmc.executebuiltin('EnableAddon("repository.emad.gitea")')
#xbmc.executebuiltin('EnableAddon("repository.emad.github")')
#xbmc.executebuiltin('EnableAddon("repository.emad.codeberg")')
#xbmc.executebuiltin('EnableAddon("plugin.video.arabicvideos")')
#xbmc.executebuiltin('EnableAddon("skin.metropolisEMAD")')


seq = seq+1
INSTALL_ADDON(seq,'plugin.video.arabicvideos')
version = ADDON_VERSION('plugin.video.arabicvideos')
SHOW_AV_VERSION(window,dialog.lang,version)


seq = seq+1
INSTALL_ADDON(seq,'skin.metropolisEMAD')
version = ADDON_VERSION('skin.metropolisEMAD')
SHOW_SKIN_VERSION(window,dialog.lang,version)


#INSTALL_ADDON('+3','resource.language.ar_sa')
"""


xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"addons.updatemode","value":0}}')
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"general.addonnotifications","value":false}}')


UPDATE_LOCAL_ADDONS()


xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.metropolisEMAD"}}')
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.estuary"}}')
time.sleep(1)
xbmc.executebuiltin('SendClick(11)')
time.sleep(1)
xbmc.log('skin.installEMAD ========= Skin changed to MetropolisEMAD',level=loglevel)


DIALOG_BUSY('stop')
xbmc.log('skin.installEMAD ========= KODIEMAD installation finished',level=loglevel)


# does not work and better without it so it can try installing again
#DIALOG_BUSY('start')
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"skin.installEMAD","enabled":false}}')
#time.sleep(5)
#xbmc.log('skin.installEMAD ========= Skin installEMAD disabled',level=loglevel)
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"setting.level":{"default":"expert"}}')
#time.sleep(5)
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"locale.country","value":"Australia (12h)"}}')
#time.sleep(5)
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"videoplayer.errorinaspect","value":"20"}}')
#time.sleep(5)
#xbmc.executebuiltin('UpdateLocalAddons')
#time.sleep(10)

