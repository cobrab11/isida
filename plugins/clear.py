#!/usr/bin/python
# -*- coding: utf -*-

def hidden_clear(type, jid, nick, text):
	try: cntr = int(text)
	except: cntr = GT('clear_default_count')
	if cntr > GT('clear_max_count'): cntr = GT('clear_max_count')
	elif cntr < 2: cntr = 2
	cdel,cmode = GT('clear_delay'),get_config(getRoom(jid),'clear_answer') == 'presence'
	clear_msg = L('Clean by %s messages in approximately %s sec.') % (str(cntr),str(int(cntr*cdel)))
	if cmode: caps_and_send(Presence(jid,show=Settings['status'], status=clear_msg, priority=Settings['priority']))
	else: send_msg(type, jid, nick, clear_msg)
	time.sleep(cdel)
	for tmp in range(0,cntr):
		sender(xmpp.Message(jid, '', "groupchat"))
		time.sleep(cdel)
	if cmode: caps_and_send(Presence(jid,show=Settings['status'], status=Settings['message'], priority=Settings['priority']))
	else: send_msg(type, jid, nick, L('Cleaned!'))

global execute

execute = [(7, 'clear', hidden_clear, 2, L('Hidden cleaning of conference history.'))]
