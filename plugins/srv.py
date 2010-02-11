#!/usr/bin/python
# -*- coding: utf -*-

def srv_nslookup(type, jid, nick, text):
	srv_raw_check(type, jid, nick, u'nslookup '+text)

def srv_dig(type, jid, nick, text):
	srv_raw_check(type, jid, nick, u'dig '+text)

def srv_host(type, jid, nick, text):
	srv_raw_check(type, jid, nick, u'host '+text)

def srv_raw_check(type, jid, nick, text):
	if text.count('&') or text.count(';'): msg = L('Unavailable!')
	else: msg = shell_execute(text)
	send_msg(type, jid, nick, msg)

def chkserver(type, jid, nick, text):
	if text.count('.') and text.count(':') and len(text) > 5:
		if text.count(' '):
			try: mtype = int(text.split(' ')[1])
			except: mtype = 1
			if mtype < 1: mtype = 1
			elif mtype >5: mtype = 5
			text = text.split(' ')[0]
		else: mtype = 1
		url = u'http://status.blackout-gaming.net/status.php?dns='+text.replace(':','&port=')+u'&style=t'+str(mtype)
		body = urllib.urlopen(url).read()
		body = (body.split('("')[1])[:-3]
		msg = L('Port status at %s') % body
	else: msg = L('What?')
	send_msg(type, jid, nick, msg)

global execute

execute = [(1, u'nslookup', srv_nslookup, 2, L('Command nslookup')),
		   (1, u'host', srv_host, 2, L('Command host')),
		   (1, u'dig', srv_dig, 2, L('Command dig')),
		   (0, u'port', chkserver, 2, L('Check port activity\nport server:port [1..5]'))]
