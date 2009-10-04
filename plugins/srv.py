#!/usr/bin/python
# -*- coding: utf -*-

def srv_nslookup(type, jid, nick, text):
	srv_raw_check(type, jid, nick, u'nslookup '+text)

def srv_dig(type, jid, nick, text):
	srv_raw_check(type, jid, nick, u'dig '+text)

def srv_host(type, jid, nick, text):
	srv_raw_check(type, jid, nick, u'host '+text)

def srv_raw_check(type, jid, nick, text):
	if text.count('&') or text.count(';'): msg = u'Недоступно!'
	else: msg = shell_execute(text)
	send_msg(type, jid, nick, msg)

global execute

execute = [(1, u'nslookup', srv_nslookup, 2, u'команда nslookup'),
		   (1, u'host', srv_host, 2, u'команда host'),
		   (1, u'dig', srv_dig, 2, u'команда dig')]
