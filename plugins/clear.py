#!/usr/bin/python
# -*- coding: utf -*-

clear_delay = 1.3

def hidden_clear(type, jid, nick, text):
	try: cntr = int(text)
	except: cntr = 20
	if cntr < 1 or cntr > 100: cntr = 20
	pprint('clear: '+unicode(jid)+' by: '+unicode(nick))
	send_msg(type, jid, nick, L('Clean by %s messages in approximately %s sec.') % (str(cntr),str(int(cntr*clear_delay))))
	time.sleep(clear_delay)
	for tmp in range(0,cntr):
		cl.send(xmpp.Message(jid, '', "groupchat"))
		time.sleep(clear_delay)
	send_msg(type, jid, nick, L('Cleaned!'))

global execute

execute = [(1, 'clear', hidden_clear, 2, L('Hidden cleaning of conference history.'))]
