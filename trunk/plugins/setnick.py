#!/usr/bin/python
# -*- coding: utf-8 -*-

def set_nickname(type, jid, nick, text):
	if get_affiliation(jid,nick) == 'owner' or get_level(jid,nick)[0] == 9:
		msg = None
		if text == '': text = jid+'/'+nickname
		else: text = jid+'/'+text
	else: msg = L('You can\'t do it!')
	if msg: send_msg(type, jid, nick, msg)
	else: bot_join(type, jid, nick, text)

global execute

execute = [(8, 'setnick', set_nickname, 2, L('Change bot nick. Available only for conference owner.'))]
