#!/usr/bin/python
# -*- coding: utf -*-

def thread_info(type, jid, nick):
	msg = u'Активно: '
	for tmp in threading.enumerate():
		te = str(tmp)[1:-2]
		msg += '\n'+ te.split('(')[1].replace(', ',' - ').replace('|',' ')
	send_msg(type, jid, nick, msg)

def thread_raw(type, jid, nick):
	msg = u'Активно тредов: '+str(threading.activeCount())
	for tmp in threading.enumerate(): msg += '\n'+str(tmp)[1:-1]
	send_msg(type, jid, nick, msg)

def thread_count(type, jid, nick):
	msg = u'Выполнено: '+str(th_cnt)+u', Активно: '+str(threading.activeCount())
	send_msg(type, jid, nick, msg)

global execute

execute = [(2, u'th', thread_info, 1, u'Список активных тредов'),
		   (2, u'th_cnt', thread_count, 1, u'Количество тредов'),
		   (2, u'th_raw', thread_raw, 1, u'Список активных тредов без разбивки')]
