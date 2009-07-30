#!/usr/bin/python
# -*- coding: utf -*-

def svn_get(type, jid, nick,text):
	tlog = 'tempo.log'
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
			except:
				revn = 0
	else:
		url=text
	if revn != 0: sh_exe = 'svn log '+url+' -r'+str(revn)
	else:
		if count > 10: count = 10
		sh_exe = 'svn log '+url+' --limit '+str(count)
	try:
		sh_ex = "bash -c '%s' 2>&1"%(sh_exe.replace("'","'\\''"))
		p = os.popen(sh_ex)
		result = p.read().decode('utf8', 'replace')
		p.close()
		msg = url+'\n'+result
	except: msg = u'Произошла ошибка обработки команды'
	send_msg(type, jid, nick, msg)
	
global execute

execute = [(0, u'svn', svn_get, 2, u'Показ svn-лога.\nsvn [http://]url [limit] - показ последней ревизий или нескольких, если указан параметр limit\nsvn [http://]url rXXX - показ ревизии с номером XXX')]
