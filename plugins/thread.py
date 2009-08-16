#!/usr/bin/python
# -*- coding: utf -*-

def thread_info(type, jid, nick):
	msg = u'Активно тредов: '+str(threading.activeCount())
	for tmp in threading.enumerate():
		stmp = str(tmp)
		msg += '\n'+stmp[stmp.find('(')+1:stmp.find(')')]
	msg = msg[:-2]
	send_msg(type, jid, nick, msg)

global execute

execute = [(2, u'thread', thread_info, 1, u'Список активных тредов')]
