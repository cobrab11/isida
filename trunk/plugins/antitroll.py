#!/usr/bin/python
# -*- coding: utf -*-

def troll(type, jid, nick, text):
	text = text.split('\n')
	r = unicode(text[0])
	try: count = int(text[2])
	except: count = GT('troll_default_limit')
	if count > GT('troll_max_limit'): count = GT('troll_max_limit')
	otake = JID(node=getName(jid), domain=getServer(jid), resource=r)
	otake = unicode(otake)
	if len(text)>1: message = text[1]
	else: message = L('You troll!')
	tst = GT('troll_sleep_time')
	while count != 0:
		sender(xmpp.Message(otake, message, "chat"))
		sleep(tst)
		count -= 1
	send_msg(type, jid, nick, L('Done'))

global execute, timer

timer = []

execute = [(9, 'troll', troll, 2, L('Repeat message to private.\ntroll nick\n[text]\n[number]'))]
