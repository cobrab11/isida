#!/usr/bin/python
# -*- coding: utf -*-

def svn_get(type, jid, nick,text):
	if text[:7] !='http://' and text[:8] !='https://' and text[:6] !='svn://': text = 'http://'+text
	count = 1
	revn = 0
	if text.count(' '):
		text = text.split(' ')
		url = text[0]
		try: count = int(text[1])
		except:
			try:
				if text[1].lower().count('r'): revn = int(text[1][text[1].find('r')+1:])
			except: revn = 0
	else: url=text
	if revn != 0: sh_exe = 'svn log '+url+' -r'+str(revn)
	else:
		if count > 10: count = 10
		sh_exe = 'svn log '+url+' --limit '+str(count)
	msg = u'SVN from '+url+'\n'+shell_execute(sh_exe)
	send_msg(type, jid, nick, msg)
	
global execute

execute = [(0, u'svn', svn_get, 2, u'Показ svn-лога.\nsvn [http://]url [limit] - показ последней ревизий или нескольких, если указан параметр limit\nsvn [http://]url rXXX - показ ревизии с номером XXX')]
