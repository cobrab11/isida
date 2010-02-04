#!/usr/bin/python
# -*- coding: utf -*-

def troll(type, jid, nick, text):
	text = text.split('\n')
	r = unicode(text[0])
	try: count = int(text[2])
	except: count = 10
	if count > 100: count = 100
	otake = JID(node=getName(jid), domain=getServer(jid), resource=r)
	otake = unicode(otake)
	pprint(u'Troll: '+unicode(otake))
	if len(text)>1: message = text[1]
	else: message = L('You troll!')
	while count != 0:
		cl.send(xmpp.Message(otake, message, "chat"))
		sleep(0.05)
		count -= 1
	send_msg(type, jid, nick, L('Done'))

global execute, timer

timer = []

execute = [(2, u'troll', troll, 2, L('Repeat messate to private.\ntroll nick\n[text]\n[number]'))]
