#!/usr/bin/python
# -*- coding: utf -*-

def is_true(type, jid, nick, text):
	if text == '':
		msg = u'Ну и?'
	else:
		idx = 0
		for tmp in text:
			idx += ord(tmp)
		idx = int((idx/100.0 - int(idx/100))*100)
		msg = u'Вероятность выражения - '+str(idx)+u'%'
	send_msg(type, jid, nick, msg)

global execute

execute = [(0, u'true', is_true, 2)]
