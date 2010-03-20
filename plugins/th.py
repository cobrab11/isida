#!/usr/bin/python
# -*- coding: utf -*-

def thread_info(type, jid, nick):
	if thread_type:
		msg = ''
		for tmp in threading.enumerate(): msg += '\n' + unicode(tmp).split('(',1)[1].split(')',1)[0]
		msg = '\nActive: %s%s' % (threading.activeCount(),msg)
	else: msg = ''
	msg = L('Executed threads: %s | Error(s): %s') % (str(th_cnt),str(thread_error_count)) + msg
	send_msg(type, jid, nick, msg)

global execute

execute = [(1, 'th', thread_info, 1, L('Threads statistic'))]
