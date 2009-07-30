#!/usr/bin/python
# -*- coding: utf -*-

def srv_shell(text):
	try:
		cmd = "bash -c '%s' 2>&1"%(text.replace("'","'\\''"))
		p = popen2.Popen3(cmd, True)
		while p.poll() == -1: pass
		msg = concat(p.fromchild.readlines()).decode('utf-8')
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
