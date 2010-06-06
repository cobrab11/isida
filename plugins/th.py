#!/usr/bin/python
# -*- coding: utf -*-

def thread_info(type, jid, nick):
	if thread_type:
		msg,tmas = '',[]
		for tmp in threading.enumerate(): tmas.append(unicode(tmp).split('(',1)[1].split(')',1)[0])
		tmas.sort()
		for tmp in tmas: msg += '\n' + tmp
		msg = '\nActive: %s%s' % (threading.activeCount(),msg)
	else: msg = ''
	msg = L('Executed threads: %s | Error(s): %s') % (th_cnt,thread_error_count) + msg
	send_msg(type, jid, nick, msg)

global execute

execute = [(7, 'th', thread_info, 1, L('Threads statistic'))]
