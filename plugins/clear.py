#!/usr/bin/python
# -*- coding: utf -*-

def hidden_clear(type, jid, nick, text):
	try: cntr = int(text)
	except: cntr = clear_default_count
	if cntr > clear_max_count: cntr = clear_max_count
	elif cntr < 2: cntr = 2
	pprint('clear: '+unicode(jid)+' by: '+unicode(nick))
	send_msg(type, jid, nick, L('Clean by %s messages in approximately %s sec.') % (str(cntr),str(int(cntr*clear_delay))))
	time.sleep(clear_delay)
	for tmp in range(0,cntr):
		sender(xmpp.Message(jid, '', "groupchat"))
		time.sleep(clear_delay)
	send_msg(type, jid, nick, L('Cleaned!'))

global execute

execute = [(7, 'clear', hidden_clear, 2, L('Hidden cleaning of conference history.'))]
