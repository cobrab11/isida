#!/usr/bin/python
# -*- coding: utf -*-

def thread_info(type, jid, nick): send_msg(type, jid, nick, L('Executed threads: %s | Error(s): %s') % (str(th_cnt),str(thread_error_count)))

global execute

execute = [(1, 'th', thread_info, 1, L('Threads statistic'))]
