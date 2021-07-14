# -*- coding: utf-8 -*-

import xbmc,time,re,xbmcgui,os,xbmcaddon

#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"locale.keyboardlayouts","value":"Arabic QWERTY|English QWERTY"}}')
#xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"addons.unknownsources","value":true}}')

userfolder = xbmc.translatePath('special://home')
useraddonsfolder = os.path.join(userfolder,'addons')
skinaddonfile = os.path.join(useraddonsfolder,'skin.metropolisEMAD','addon.xml')
arabicaddonfile = os.path.join(useraddonsfolder,'plugin.video.arabicvideos','addon.xml')

masterfolder = xbmc.translatePath('special://xbmc')
installskinaddonfile = os.path.join(masterfolder,'addons','skin.installEMAD','addon.xml')

xbmc.executebuiltin('UpdateAddonRepos')
#xbmc.executebuiltin('UpdateLocalAddons')

kodi_release = xbmc.getInfoLabel("System.BuildVersion")
kodi_version = re.findall('&&(.*?)[ -]','&&'+kodi_release,re.DOTALL)
kodi_version = float(kodi_version[0])

addonscount = 50
pDialog = xbmcgui.DialogProgress()
pDialog.create('يجري الآن جلب وتحديث إضافات كودي من الإنترنيت')

count = 1
for i in range(720):
	if os.path.exists(skinaddonfile) and os.path.exists(arabicaddonfile):
		break
	pDialog.update(int(100*count/addonscount),'يرجى الانتظار والصبر ... جلب الإضافة رقم',str(count)+'/'+str(addonscount))
	if pDialog.iscanceled():
		xbmc.executebuiltin('Quit')
		sys.exit()
	try: count = len(os.listdir(useraddonsfolder))
	except: pass
	time.sleep(5)

if i<=719:
	result = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"skin.metropolisEMAD"}}')
	time.sleep(1)
	xbmc.executebuiltin('SendClick(11)')
	masterfolder = xbmc.translatePath('special://xbmc')
	pDialog.close()
else:
	pDialog.close()
	xbmcgui.Dialog().ok('التثبيت أخذ وقت طويل جدا','للأسف فشل في تثبيت إضافات كودي ... جرب مسح كل شيء وبعدها حاول مرة اخرى')




#result = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":false}}' % 'skin.installEMAD')
#xbmc.log('EMAD ========= '+str(result), level=xbmc.LOGNOTICE)
#installskinaddonfile = os.path.join(masterfolder,'addons','skin.installEMAD','addon.xml')
#os.remove(installskinaddonfile)
#installskinaddonfile = os.path.join(masterfolder,'addons','skin.installEMAD','MAIN.py')
#os.remove(installskinaddonfile)
#try:
#installskinaddonfile = os.path.join(masterfolder,'addons','skin.installEMAD','720p','Home.xml')
#os.remove(installskinaddonfile)
#except: pass
