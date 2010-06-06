#!/usr/bin/python
# -*- coding: utf -*-

def md5body(type, jid, nick, text):
	if len(text): msg = hashlib.md5(text.encode('utf-8')).hexdigest()
	else: msg = L('What?')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'md5', md5body, 2, L('Calculate phrase md5 sum.'))]
