#!/usr/bin/python
# -*- coding: utf -*-

def srv_shell(text):
	try:
		sh_ex = "bash -c '%s' 2>&1"%(text.replace("'","'\\''"))
		p = os.popen(sh_ex)
		msg = p.read().decode('utf8', 'replace')
	except: msg = u'Произошла ошибка обработки команды'
	return msg

def srv_nslookup(type, jid, nick, text):
	msg = srv_shell(u'nslookup '+text)
	send_msg(type, jid, nick, msg)

def srv_dig(type, jid, nick, text):
	msg = srv_shell(u'dig '+text)
	send_msg(type, jid, nick, msg)

def srv_host(type, jid, nick, text):
	msg = srv_shell(u'host '+text)
	send_msg(type, jid, nick, msg)

global execute

execute = [(1, u'nslookup', srv_nslookup, 2, u'команда nslookup'),
		   (1, u'host', srv_host, 2, u'команда host'),
		   (1, u'dig', srv_dig, 2, u'команда dig')]
