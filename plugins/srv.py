#!/usr/bin/python
# -*- coding: utf -*-

def srv_nslookup(type, jid, nick, text):
	msg = shell_execute(u'nslookup '+text)
	send_msg(type, jid, nick, msg)

def srv_dig(type, jid, nick, text):
	msg = shell_execute(u'dig '+text)
	send_msg(type, jid, nick, msg)

def srv_host(type, jid, nick, text):
	msg = shell_execute(u'host '+text)
	send_msg(type, jid, nick, msg)

global execute

execute = [(1, u'nslookup', srv_nslookup, 2, u'команда nslookup'),
		   (1, u'host', srv_host, 2, u'команда host'),
		   (1, u'dig', srv_dig, 2, u'команда dig')]
