#!/usr/bin/python
# -*- coding: utf -*-

def md5body(type, jid, nick, text):
	if len(text): msg = hashlib.md5(text.encode('utf-8')).hexdigest()
	else: msg = u'Ась?'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'md5', md5body, 2, u'Расчёт md5 фразы.')]
