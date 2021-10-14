# -*- coding: utf-8 -*-


import sys,urllib2,re,xbmcaddon,os,xbmc,platform,uuid,hashlib,random,xbmcgui,time,threading


xbmcfolder = xbmc.translatePath('special://xbmc')
xbmcaddonsfolder = os.path.join(xbmcfolder,'addons')
userfolder = xbmc.translatePath('special://home')
useraddonsfolder = os.path.join(userfolder,'addons')


def HIGEST_REPOSITORIES_VERSION():
	ver1 = ADDON_VERSION('repository.emad')
	ver2 = ADDON_VERSION('repository.emad.github')
	ver3 = ADDON_VERSION('repository.emad.gitea')
	ver4 = ADDON_VERSION('repository.emad.codeberg')
	max_ver = max(ver1,ver2,ver3,ver4)
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
		with open(addonfile,'r') as f: xmlfile = f.read()
		version = re.findall('id=[\"\'](.*?)[\"\'].*?version=[\"\'](.*?)[\"\']',xmlfile,re.DOTALL|re.IGNORECASE)
		if version: id,ver = version[0]
	except: pass
	return ver


def dummyClientID(length):
	#addon_id = ''
	#addon_version = ADDON_VERSION(addon_id)
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
	addon_version = ADDON_VERSION('skin.installEMAD')
	website = 'INSTALL'
	kodi_release = xbmc.getInfoLabel("System.BuildVersion")
	kodi_version = re.findall('&&(.*?)[ -]','&&'+kodi_release,re.DOTALL)
	kodi_version = str(float(kodi_version[0]))
	randomNumber = str(random.randrange(111111111111,999999999999))
	try:
		headers = {'User-Agent':''}
		url = 'http://www.google-analytics.com/collect?v=1&tid=UA-127045104-5&cid='+dummyClientID(32)+'&t=event&sc=end&ec='+addon_version+'&av='+addon_version+'&an=ARABIC_VIDEOS&ea='+website+'&el='+kodi_version+'&z='+randomNumber
		request = urllib2.Request(url=url,headers=headers)
		response = urllib2.urlopen(request)
		xbmc.log('skin.installEMAD ========= Sent analytics',level=xbmc.LOGNOTICE)
		#html = response.read()
	except: pass
	return


def BUSY_DIALOG(job):
	# dialog = 'busydialog'				# KODI 17.9 and earlier
	dialog = 'busydialognocancel'		# KODI 18 and later
	if job=='start': xbmc.executebuiltin('ActivateWindow('+dialog+')')
	elif job=='stop': xbmc.executebuiltin('Dialog.Close('+dialog+')')
	return


def SHOW_AV_VERSION(window22,lang,version):
	if lang=='ar': text1 = text_av_ver_ar+'\n('+version+')'
	else: text1 = text_av_ver_en+'\n('+version+')'
	window22.getControl(9003).setLabel(text1)
	return


def SHOW_SKIN_VERSION(window22,lang,version):
	if lang=='ar': text2 = text_skin_ver_ar+' ('+version+')[COLOR FFC89008]كودي: [/COLOR]'
	else: text2 = text_skin_ver_en+'('+version+')'
	window22.getControl(9004).setLabel(text2)
	return


def SHOW_REPOS_VERSION(window22,lang,version):
	if lang=='ar': text1 = '('+version+')'+text_repos_ver_ar
	else: text1 = text_repos_ver_en+'('+version+')'
	window22.getControl(9005).setLabel(text1)
	return


def UPDATE_REPOS(seq,delay=10):
	xbmc.executebuiltin('UpdateAddonRepos')
	xbmc.log('skin.installEMAD ========= Executed UpdateAddonRepos '+str(seq),level=xbmc.LOGNOTICE)
	time.sleep(delay)
	return


if 'mode=1' in sys.argv[2]:
	SEND_ANALYTICS_EVENT()
	sys.exit()


xbmc.log('skin.installEMAD ========= KODIEMAD Installation started',level=xbmc.LOGNOTICE)


BUSY_DIALOG('start')


progressbar_totaltime = 720
button0,button1,button2 = 'عربي','English','إلغاء - Quit'
textAR = 'بدأ كودي الآن تحديث نفسه وتثبيت جميع الإضافات . الرجاء الانتظار 12 دقيقة'
textEN = 'Kodi started now to update itself and install all addons . Please wait for 12 minutes'
arabic_big_text = 'سوف يبدأ برنامج كودي الإصدار رقم 18.9 الآن عملية تثبيت برنامج عماد للفيديوهات العربية ومعه جلد عماد متروبولس ومعه مخازن عماد ... عند نهاية هذه العملية سوف تختفي هذه الشاشة ويظهر بدلا منها القائمة الرئيسية لبرنامج كودي ومعها برنامج عماد ... حجم التحميل المتوقع هو تقريبا 100 ميغابايت وهذه تحتاج وقت تقريبا 10 دقائق لتحميل الملفات من الأنترنيت وتثبيتها في كودي ... قد تحتاج وقت اكثر إذا الأنترنيت عندك بطيئة أو جهازك بطيء ... أهمل رسائل الخطأ في هذه الشاشة ... في حال حدوث مشكلة قم بمسح كل شيء وابدأ من جديد'
english_big_text = 'KODI software version 18.9 will start now the install of EMAD Arabic Videos with EMAD metropolis skin with EMAD Repositories . At the end of this process the screen will switch to KODI main menu and EMAD Arabic Videos . The download size expected is 100 MegaByte and this might need 10 minutes to download the files and install them on KODI . Slow internet or slow device will need more time . Ignore error messages in this screen . If you get problems then delete everything and start again'
text_av_ver_ar = '[COLOR FFC89008]رقم إصدار برنامج عماد في كودي:[/COLOR]'
text_av_ver_en = '[COLOR FFC89008]Version of Arabic Videos in Kodi:[/COLOR]'
text_skin_ver_ar = '[COLOR FFC89008]رقم إصدار جلد متروبولس عماد في[/COLOR]'
text_skin_ver_en = '[COLOR FFC89008]Version of skin metropolisEMAD\nin Kodi: [/COLOR]'
text_repos_ver_ar = '[COLOR FFC89008]رقم إصدار مخازن عماد في كودي: [/COLOR]'
text_repos_ver_en = '[COLOR FFC89008]Version of EMAD Repositories in Kodi: [/COLOR]'


window = xbmcgui.Window(10000)
window.getControl(9001).setLabel(arabic_big_text)
version = HIGEST_REPOSITORIES_VERSION()
SHOW_REPOS_VERSION(window,'ar',version)
version = ADDON_VERSION('plugin.video.arabicvideos')
SHOW_AV_VERSION(window,'ar',version)
version = ADDON_VERSION('skin.metropolisEMAD')
SHOW_SKIN_VERSION(window,'ar',version)


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
	count_old,time_old,seq = 0,0,0
	for ii in range(progressbar_totaltime):
		time.sleep(1)
		timeTEXT = time.strftime("%M:%S",time.gmtime(progressbar_totaltime-ii))
		header = 'وقت متبقي:   '+timeTEXT+'   :Time Remaining'
		dialog22.getControl(1).setLabel(header)
		percent = int(100*ii/progressbar_totaltime)
		dialog22.getControl(20).setPercent(percent)
		if ii==0: xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"service.xbmc.versioncheck","enabled":false}}')
		if ii==4: xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":"1","params":{"setting":"screensaver.mode","value":""}}')
		if ii<8: continue
		if ii%60==8:
			seq = seq+1
			UPDATE_REPOS(seq,0)
		if ii%30==12:
			addon1_ver_new = HIGEST_REPOSITORIES_VERSION()
			if addon1_ver_new!=addon1_ver_old:
				addon1_ver_old = addon1_ver_new
				SHOW_REPOS_VERSION(window22,dialog22.lang,addon1_ver_new)
				xbmc.log('skin.installEMAD ========= 1st repository.emad.* '+addon1_ver_new+' installed',level=xbmc.LOGNOTICE)
		if ii%30==16:
			addon2_ver_new = ADDON_VERSION('plugin.video.arabicvideos')
			if addon2_ver_new!=addon2_ver_old:
				addon2_ver_old = addon2_ver_new
				SHOW_AV_VERSION(window22,dialog22.lang,addon2_ver_new)
				xbmc.log('skin.installEMAD ========= 1st plugin.video.arabicvideos '+addon2_ver_new+' installed',level=xbmc.LOGNOTICE)
		if ii%30==20:
			addon3_ver_new = ADDON_VERSION('skin.metropolisEMAD')
			if addon3_ver_new!=addon3_ver_old:
				addon3_ver_old = addon3_ver_new
				SHOW_SKIN_VERSION(window22,dialog22.lang,addon3_ver_new)
				xbmc.log('skin.installEMAD ========= 1st skin.metropolisEMAD '+addon3_ver_new+' installed',level=xbmc.LOGNOTICE)
		if ii%30==24:
			addon4_ver_new = ADDON_VERSION('resource.language.ar_sa')
			if addon4_ver_new!=addon4_ver_old:
				addon4_ver_old = addon4_ver_new
				xbmc.log('skin.installEMAD ========= 1st resource.language.ar_sa '+addon4_ver_new+' installed',level=xbmc.LOGNOTICE)
		if ii%30==28:
			count_new = len(os.listdir(useraddonsfolder))
			time_new = time.time()
			if count_new>count_old: count_old,time_old = count_new,time_new
			elif 170<time_new-time_old<190: break
		if ii%30==2:
			installed = addon1_ver_old>zero and addon2_ver_old>zero and addon3_ver_old>zero and addon4_ver_old>zero
			if installed: break
			"""
			files_count = 0
			addonfolder = os.path.join(useraddonsfolder,'skin.metropolisEMAD')
			for root,dirs,files in os.walk(addonfolder):
				files_count += len(files)
			#dialog22.getControl(9).setText(str(files_count))
			#time.sleep(5)
			if files_count>700: break
			"""
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
th = threading.Thread(target=updateProgressBar,args=(dialog,window,))
th.start()
dialog.getControl(9).setText(textAR)
while dialog.controlID==-1:
	dialog.doModal()
	if dialog.controlID==-1:
		xbmc.log('skin.installEMAD ========= User requested Escape',level=xbmc.LOGNOTICE)
	elif dialog.controlID==10:
		xbmc.log('skin.installEMAD ========= User requested Arabic',level=xbmc.LOGNOTICE)
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
		xbmc.log('skin.installEMAD ========= User requested English',level=xbmc.LOGNOTICE)
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
		xbmc.log('skin.installEMAD ========= User requested Quit',level=xbmc.LOGNOTICE)
		xbmc.executebuiltin('Quit()')
		sys.exit()
	elif dialog.controlID==99:
		xbmc.log('skin.installEMAD ========= ProgressBar closed',level=xbmc.LOGNOTICE)
		break
	dialog.controlID = -1


"""
def INSTALL_ADDON(seq,addon_id):
	addon_ver = ADDON_VERSION(addon_id)
	if not addon_ver>'0.0.0.0':
		UPDATE_REPOS(seq)
		xbmc.executebuiltin('InstallAddon('+addon_id+')')
		time.sleep(1)
		xbmc.executebuiltin('SendClick(11)')
		while xbmc.getCondVisibility('Window.IsActive(progressdialog)'): time.sleep(1)
		xbmc.log('skin.installEMAD ========= 2nd '+addon_id+' installed',level=xbmc.LOGNOTICE)
	return

INSTALL_ADDON(101,'plugin.video.arabicvideos')
version = ADDON_VERSION('plugin.video.arabicvideos')
SHOW_AV_VERSION(window,dialog.lang,version)

INSTALL_ADDON(102,'skin.metropolisEMAD')
version = ADDON_VERSION('skin.metropolisEMAD')
SHOW_SKIN_VERSION(window,dialog.lang,version)

INSTALL_ADDON(103,'resource.language.ar_sa')
"""


xbmc.executebuiltin('UpdateLocalAddons')
xbmc.log('skin.installEMAD ========= Executed UpdateLocalAddons',level=xbmc.LOGNOTICE)
time.sleep(10)


xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.metropolisEMAD"}}')
time.sleep(1)
xbmc.executebuiltin('SendClick(11)')
xbmc.log('skin.installEMAD ========= Skin changed to MetropolisEMAD',level=xbmc.LOGNOTICE)


BUSY_DIALOG('stop')
xbmc.log('skin.installEMAD ========= KODIEMAD Installation succeeded',level=xbmc.LOGNOTICE)


# does not work and better without it so it can try installing again
#BUSY_DIALOG('start')
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"skin.installEMAD","enabled":false}}')
#time.sleep(5)
#xbmc.log('skin.installEMAD ========= Skin installEMAD disabled',level=xbmc.LOGNOTICE)
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":"1","setting.level":{"default":"expert"}}')
#time.sleep(5)
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":"1","params":{"setting":"locale.country","value":"Australia (12h)"}}')
#time.sleep(5)
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"videoplayer.errorinaspect","value":"20"}}')
#time.sleep(5)
#xbmc.executebuiltin('UpdateLocalAddons')
#time.sleep(10)

