#!/usr/bin/python
# -*- coding: utf-8 -*-

def set_nickname(type, jid, nick, text):
	if get_affiliation(jid,nick) == 'owner' or get_access(jid,nick)[0] == 2:
		msg = None
		if text == '': text = jid+'/'+nickname
		else: text = jid+'/'+text
	else: msg = u'Тибе низя!'
	if msg: send_msg(type, jid, nick, msg)
	else: bot_join(type, jid, nick, text)

global execute

execute = [(1, u'setnick', set_nickname, 2, u'Смена ника. Доступна только владельцу конференции.')]
