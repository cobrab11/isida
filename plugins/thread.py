#!/usr/bin/python
# -*- coding: utf -*-

def thread_info(type, jid, nick):
	msg = u'Активно тредов: '+str(threading.activeCount())
	for tmp in threading.enumerate(): msg += '\n'+str(tmp)
	send_msg(type, jid, nick, msg)

global execute

execute = [(2, u'thread', thread_info, 1, u'Список активных тредов')]
