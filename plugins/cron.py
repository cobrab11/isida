#!/usr/bin/python
# -*- coding: utf -*-

cron_base = set_folder+u'cron.db'	# база заданий

def time_cron(type, jid, nick, text):
	send_msg(type, jid, nick, msg)

def cron_action():
	return

global execute, timer

timer = [cron_action]

execute = [(2, u'cron', time_cron, 2, u'...')]
