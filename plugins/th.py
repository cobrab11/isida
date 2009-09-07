#!/usr/bin/python
# -*- coding: utf -*-

def thread_info(type, jid, nick):
	send_msg(type, jid, nick, u'Выполнено тредов: '+str(th_cnt)+u' | Ошибок исполнения тредов: '+str(thread_error_count))

global execute

execute = [(1, u'th', thread_info, 1, u'Статистика работы тредов')]
